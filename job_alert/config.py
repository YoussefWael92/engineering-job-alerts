# Personal engineering-job profile.
# Edit these lists to tune the alerts.

KEYWORDS = [
    # Hardware / semiconductor
    "electronics",
    "electrical engineering",
    "hardware",
    "semiconductor",
    "asic",
    "soc",
    "vlsi",
    "eda",
    "ic design",
    "integrated circuit",

    # Digital design / verification
    "digital design",
    "rtl",
    "verilog",
    "systemverilog",
    "uvm",
    "verification",
    "design verification",
    "functional verification",
    "formal verification",
    "fpga",
    "digital logic",

    # Embedded / firmware
    "embedded",
    "firmware",
    "microcontroller",
    "mcu",
    "stm32",
    "arm",
    "embedded systems",

    # Analog / RF / mixed signal
    "analog",
    "mixed signal",
    "rf",
    "radio frequency",
    "cmos",
    "layout",
    "physical design",

    # Software that supports the hardware path
    "python",
    "c",
    "c++",
    "linux",
    "automation",
    "test automation",
    "software test",
    "validation",
]

ROLE_KEYWORDS = [
    "intern",
    "internship",
    "student",
    "co-op",
    "working student",
    "new graduate",
    "graduate",
    "junior",
    "trainee",
    "entry level",
    "early career",
]

PREFERRED_LOCATIONS = [
    "egypt",
    "cairo",
    "new cairo",
    "united states",
    "usa",
    "remote",
]

# Jobs below this score are ignored.
MIN_SCORE = 5

# Company sources. The HTML sources are deliberately conservative:
# if a company's page changes, the job monitor should fail gracefully.
COMPANIES = [
    {
        "name": "Bosch",
        "type": "smartrecruiters",
        "identifier": "BoschGroup",
        "url": "https://careers.smartrecruiters.com/BoschGroup/egypt",
    },
    {
        "name": "Mixel / Silvaco",
        "type": "smartrecruiters",
        "identifier": "Silvaco1",
        "url": "https://careers.smartrecruiters.com/Silvaco1/mixel-of-silvaco",
        # SmartRecruiters hosts Mixel as a Silvaco microsite. The adapter
        # collects Silvaco postings and applies the normal engineering filters.
    },
    {
        "name": "Si-Ware Systems",
        "type": "recruitee",
        "subdomain": "siwaresystems",
        "url": "https://siwaresystems.recruitee.com/",
    },
    {
        "name": "SI-Vision",
        "type": "html",
        "url": "https://www.si-vision.com/career.html",
    },

    # Large-company career pages. These use the HTML fallback initially.
    # If a site's frontend changes, add a dedicated adapter later.
    {
        "name": "Analog Devices",
        "type": "html",
        "url": "https://www.analog.com/en/careers/career-opportunities.html",
    },
    {
        "name": "GlobalFoundries",
        "type": "html",
        "url": "https://gf.com/careers/",
    },
    {
        "name": "Synopsys",
        "type": "html",
        "url": "https://careers.synopsys.com/search-jobs",
    },
    {
        "name": "NVIDIA",
        "type": "html",
        "url": "https://jobs.nvidia.com/careers?location=United+States",
    },
    {
        "name": "Intel",
        "type": "html",
        "url": "https://www.intel.com/content/www/us/en/jobs/locations/united-states.html",
    },
    {
        "name": "Siemens",
        "type": "html",
        "url": "https://www.siemens.com/global/en/company/jobs.html",
    },
    {
        "name": "STMicroelectronics",
        "type": "html",
        "url": "https://careers.st.com/",
    },

    # You wrote "InfiniLink". I could not confidently identify a single
    # matching semiconductor employer from public search results, so this is
    # intentionally left as a manual URL placeholder instead of guessing.
    {
        "name": "InfiniLink",
        "type": "disabled",
        "url": "",
        "note": "Set the exact careers URL after confirming the company.",
    },
]
