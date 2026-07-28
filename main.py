import logging
from pathlib import Path
from src.modules.file_handler import FileHandler

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s"
)

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s"
)

handler = FileHandler()
handler.validate_file_exists(
    Path("C:\\Users\\ADMIN\\Downloads\\Documents\\Ayesha_PythonProjects\\6_June_Sat_Sunday_25_July_Mock_schedule.xlsx")
                             )
handler.validate_file_extension(
    # Path("C:\Users\ADMIN\Downloads\Documents\Ayesha_2026\Exam_ApplicationFroms\Recruitment of Probationary Officers ADVERTISEMENT NO_ CRPD_PO_2026-27_09_ayeshawavale.pdf")
    Path("C:\\Users\\ADMIN\\Downloads\\Documents\\Ayesha_PythonProjects\\6_June_Sat_Sunday_25_July_Mock_schedule.xlsx")

)