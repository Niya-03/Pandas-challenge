from src.data_generator import DataGenerator
from src.data_transformer import DataTransformer
from src.report_generator import ReportGenerator

def main():
    dataGenerator = DataGenerator()
    dataTransformer = DataTransformer()
    reportGenerator = ReportGenerator()

    if not dataGenerator.generate_mock_data():
        return
   
    if not dataTransformer.generate_clean_data_csv():
        return

    if not reportGenerator.generate_report():
        return
    
    print("Task finished successfully!")
    
if __name__=="__main__":
    main()

