from data_generator import DataGenerator
from data_transformer import DataTransformer
from report_generator import ReportGenerator

dataGenerator = DataGenerator()

dataGenerator.generate_products()
dataGenerator.generate_users()
dataGenerator.generate_transactions()

dataTransformer = DataTransformer()
dataTransformer.generate_clean_data_csv()

reportGenerator = ReportGenerator()
reportGenerator.generate_report()

