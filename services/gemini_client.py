import os
import time

from dotenv import load_dotenv
from google import genai


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()


# =========================================================
# MEMORY DIAGNOSTICS
# =========================================================

def get_memory_usage_mb():
    """
    Get the current Python process memory usage in MB.

    Works on:
        - Windows
        - Linux / Render

    No external package is required.
    """

    try:

        # -------------------------------------------------
        # WINDOWS
        # -------------------------------------------------

        if os.name == "nt":

            import ctypes
            from ctypes import wintypes

            class PROCESS_MEMORY_COUNTERS(
                ctypes.Structure
            ):

                _fields_ = [
                    ("cb", wintypes.DWORD),
                    ("PageFaultCount", wintypes.DWORD),
                    ("PeakWorkingSetSize", ctypes.c_size_t),
                    ("WorkingSetSize", ctypes.c_size_t),
                    ("QuotaPeakPagedPoolUsage", ctypes.c_size_t),
                    ("QuotaPagedPoolUsage", ctypes.c_size_t),
                    ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t),
                    ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
                    ("PagefileUsage", ctypes.c_size_t),
                    ("PeakPagefileUsage", ctypes.c_size_t),
                ]

            counters = PROCESS_MEMORY_COUNTERS()

            counters.cb = ctypes.sizeof(
                PROCESS_MEMORY_COUNTERS
            )

            kernel32 = ctypes.WinDLL(
                "kernel32",
                use_last_error=True
            )

            psapi = ctypes.WinDLL(
                "psapi",
                use_last_error=True
            )

            kernel32.GetCurrentProcess.restype = (
                wintypes.HANDLE
            )

            psapi.GetProcessMemoryInfo.argtypes = [
                wintypes.HANDLE,
                ctypes.POINTER(
                    PROCESS_MEMORY_COUNTERS
                ),
                wintypes.DWORD
            ]

            psapi.GetProcessMemoryInfo.restype = (
                wintypes.BOOL
            )

            process_handle = (
                kernel32.GetCurrentProcess()
            )

            success = psapi.GetProcessMemoryInfo(
                process_handle,
                ctypes.byref(counters),
                counters.cb
            )

            if not success:

                return None

            return (
                counters.WorkingSetSize
                / (1024 * 1024)
            )


        # -------------------------------------------------
        # LINUX / RENDER
        # -------------------------------------------------

        else:

            with open(
                "/proc/self/status",
                "r"
            ) as file:

                for line in file:

                    if line.startswith(
                        "VmRSS:"
                    ):

                        parts = line.split()

                        memory_kb = float(
                            parts[1]
                        )

                        return (
                            memory_kb / 1024
                        )

    except Exception as error:

        print(
            "Memory diagnostic error:",
            repr(error)
        )

    return None


def print_memory_usage(label):

    memory_mb = get_memory_usage_mb()

    if memory_mb is None:

        print(
            f"[MEMORY] {label}: "
            "Unable to determine memory usage."
        )

        return

    print(
        f"[MEMORY] {label}: "
        f"{memory_mb:.2f} MB"
    )


# =========================================================
# GET GEMINI API KEY
# =========================================================

api_key = os.getenv(
    "GEMINI_API_KEY"
)


if not api_key:

    raise ValueError(
        "GEMINI_API_KEY environment variable is not set."
    )


# =========================================================
# CREATE GEMINI CLIENT
# =========================================================

print_memory_usage(
    "Before Gemini client creation"
)


client = genai.Client(
    api_key=api_key
)


print_memory_usage(
    "After Gemini client creation"
)


# =========================================================
# RETRY SETTINGS
# =========================================================

MAX_RETRIES = 3

RETRY_DELAYS = [
    3,
    6,
    12
]


# =========================================================
# GENERATE AI RESPONSE
# =========================================================

def generate_ai_response(prompt):
    """
    Send a prompt to Gemini and return the generated response.

    Temporary Gemini 503 errors are retried automatically.

    Maximum attempts:
        1 initial request + 3 retries

    Total retry delays:
        3 + 6 + 12 seconds
    """

    # -----------------------------------------------------
    # VALIDATE PROMPT
    # -----------------------------------------------------

    if not prompt:

        raise ValueError(
            "AI prompt cannot be empty."
        )


    print(
        "\n=============================================="
    )

    print(
        "GEMINI REQUEST MEMORY DIAGNOSTICS"
    )

    print(
        "=============================================="
    )


    print_memory_usage(
        "Before Gemini API request"
    )


    print(
        "[MEMORY] Prompt characters:",
        len(prompt)
    )


    # =====================================================
    # GEMINI REQUEST WITH RETRY
    # =====================================================

    for attempt in range(
        MAX_RETRIES + 1
    ):

        try:

            print(
                f"[GEMINI] Attempt "
                f"{attempt + 1}/{MAX_RETRIES + 1}"
            )


            # -------------------------------------------------
            # API REQUEST
            # -------------------------------------------------

            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )


            # -------------------------------------------------
            # MEMORY AFTER RESPONSE
            # -------------------------------------------------

            print_memory_usage(
                "After Gemini API response"
            )


            # -------------------------------------------------
            # VALIDATE RESPONSE
            # -------------------------------------------------

            if not response:

                raise ValueError(
                    "Gemini returned an empty response."
                )


            if not response.text:

                raise ValueError(
                    "Gemini returned an empty response."
                )


            # -------------------------------------------------
            # RESPONSE INFORMATION
            # -------------------------------------------------

            print(
                "[MEMORY] Gemini response characters:",
                len(response.text)
            )


            print_memory_usage(
                "Before returning Gemini response"
            )


            print(
                "=============================================="
            )

            print(
                "GEMINI REQUEST COMPLETED"
            )

            print(
                "==============================================\n"
            )


            return response.text


        # =====================================================
        # ERROR HANDLING
        # =====================================================

        except Exception as error:

            error_message = str(
                error
            ).lower()


            print(
                "\n=============================================="
            )

            print(
                "GEMINI API ERROR"
            )

            print(
                "=============================================="
            )

            print(
                str(error)
            )


            print_memory_usage(
                "Memory after Gemini API error"
            )


            # -------------------------------------------------
            # CHECK WHETHER ERROR IS TEMPORARY
            # -------------------------------------------------

            is_temporary_error = (
                "503" in error_message
                or
                "unavailable" in error_message
                or
                "high demand" in error_message
                or
                "429" in error_message
                or
                "resource exhausted" in error_message
                or
                "rate limit" in error_message
            )


            # -------------------------------------------------
            # RETRY TEMPORARY ERRORS
            # -------------------------------------------------

            if (
                is_temporary_error
                and attempt < MAX_RETRIES
            ):

                delay = RETRY_DELAYS[
                    attempt
                ]


                print(
                    f"[GEMINI] Temporary error detected."
                )

                print(
                    f"[GEMINI] Retrying in "
                    f"{delay} seconds..."
                )


                print(
                    "==============================================\n"
                )


                time.sleep(
                    delay
                )


                continue


            # -------------------------------------------------
            # PERMANENT / FINAL ERROR
            # -------------------------------------------------

            print(
                "No more retries available."
            )


            print(
                "==============================================\n"
            )


            raise