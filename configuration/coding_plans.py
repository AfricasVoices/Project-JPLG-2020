from core_data_modules.cleaners import somali, swahili, Codes
from core_data_modules.traced_data.util.fold_traced_data import FoldStrategies

from configuration import code_imputation_functions
from configuration.code_schemes import CodeSchemes
from src.lib.configuration_objects import CodingConfiguration, CodingModes, CodingPlan


def clean_age_with_range_filter(text):
    """
    Cleans age from the given `text`, setting to NC if the cleaned age is not in the range 10 <= age < 100.
    """
    age = swahili.DemographicCleaner.clean_age(text)
    if type(age) == int and 10 <= age < 100:
        return str(age)
        # TODO: Once the cleaners are updated to not return Codes.NOT_CODED, this should be updated to still return
        #       NC in the case where age is an int but is out of range
    else:
        return Codes.NOT_CODED


def clean_district_if_no_mogadishu_sub_district(text):
    mogadishu_sub_district = somali.DemographicCleaner.clean_mogadishu_sub_district(text)
    if mogadishu_sub_district == Codes.NOT_CODED:
        return somali.DemographicCleaner.clean_somalia_district(text)
    else:
        return Codes.NOT_CODED


def get_rqa_coding_plans(pipeline_name):
    return [
        CodingPlan(raw_field="rqa_s07e01_raw",
                   time_field="sent_on",
                   run_id_field="rqa_s07e01_run_id",
                   coda_filename="s07e01.json",
                   icr_filename="s07e01.csv",
                   coding_configurations=[
                       CodingConfiguration(
                           coding_mode=CodingModes.MULTIPLE,
                           code_scheme=CodeSchemes.S07E01,
                           coded_field="rqa_s07e01_coded",
                           analysis_file_key="rqa_s07e01_",
                           fold_strategy=lambda x, y: FoldStrategies.list_of_labels(CodeSchemes.S07E01, x, y)
                       )
                   ],
                   ws_code=CodeSchemes.WS_CORRECT_DATASET.get_code_with_match_value("s07e01"),
                   raw_field_fold_strategy=FoldStrategies.concatenate),

        CodingPlan(raw_field="rqa_s07e02_raw",
                   time_field="sent_on",
                   run_id_field="rqa_s07e02_run_id",
                   coda_filename="s07e02.json",
                   icr_filename="s07e02.csv",
                   coding_configurations=[
                       CodingConfiguration(
                           coding_mode=CodingModes.MULTIPLE,
                           code_scheme=CodeSchemes.S07E02,
                           coded_field="rqa_s07e02_coded",
                           analysis_file_key="rqa_s07e02_",
                           fold_strategy=lambda x, y: FoldStrategies.list_of_labels(CodeSchemes.S07E02, x, y)
                       )
                   ],
                   ws_code=CodeSchemes.WS_CORRECT_DATASET.get_code_with_match_value("s07e02"),
                   raw_field_fold_strategy=FoldStrategies.concatenate),

        CodingPlan(raw_field="rqa_s07e03_raw",
                   time_field="sent_on",
                   run_id_field="rqa_s07e03_run_id",
                   coda_filename="s07e03.json",
                   icr_filename="s07e03.csv",
                   coding_configurations=[
                       CodingConfiguration(
                           coding_mode=CodingModes.MULTIPLE,
                           code_scheme=CodeSchemes.S07E03,
                           coded_field="rqa_s07e03_coded",
                           analysis_file_key="rqa_s07e03_",
                           fold_strategy=lambda x, y: FoldStrategies.list_of_labels(CodeSchemes.S07E03, x, y)
                       )
                   ],
                   ws_code=CodeSchemes.WS_CORRECT_DATASET.get_code_with_match_value("s07e03"),
                   raw_field_fold_strategy=FoldStrategies.concatenate)
    ]


def get_survey_coding_plans(pipeline_name):
    return [
        CodingPlan(raw_field="operator_raw",
                   coding_configurations=[
                       CodingConfiguration(
                           coding_mode=CodingModes.SINGLE,
                           code_scheme=CodeSchemes.SOMALIA_OPERATOR,
                           coded_field="operator_coded",
                           analysis_file_key="operator",
                           fold_strategy=FoldStrategies.assert_label_ids_equal
                       )
                   ],
                   raw_field_fold_strategy=FoldStrategies.assert_equal),

        CodingPlan(raw_field="location_raw",
                   time_field="location_time",
                   coda_filename="location.json",
                   coding_configurations=[
                       CodingConfiguration(
                           coding_mode=CodingModes.SINGLE,
                           code_scheme=CodeSchemes.MOGADISHU_SUB_DISTRICT,
                           cleaner=somali.DemographicCleaner.clean_mogadishu_sub_district,
                           coded_field="mogadishu_sub_district_coded",
                           analysis_file_key="mogadishu_sub_district",
                           fold_strategy=FoldStrategies.assert_label_ids_equal
                       ),
                       CodingConfiguration(
                           coding_mode=CodingModes.SINGLE,
                           code_scheme=CodeSchemes.SOMALIA_DISTRICT,
                           cleaner=clean_district_if_no_mogadishu_sub_district,
                           coded_field="district_coded",
                           analysis_file_key="district",
                           fold_strategy=FoldStrategies.assert_label_ids_equal
                       ),
                       CodingConfiguration(
                           coding_mode=CodingModes.SINGLE,
                           code_scheme=CodeSchemes.SOMALIA_REGION,
                           coded_field="region_coded",
                           analysis_file_key="region",
                           fold_strategy=FoldStrategies.assert_label_ids_equal
                       ),
                       CodingConfiguration(
                           coding_mode=CodingModes.SINGLE,
                           code_scheme=CodeSchemes.SOMALIA_STATE,
                           coded_field="state_coded",
                           analysis_file_key="state",
                           fold_strategy=FoldStrategies.assert_label_ids_equal
                       ),
                       CodingConfiguration(
                           coding_mode=CodingModes.SINGLE,
                           code_scheme=CodeSchemes.SOMALIA_ZONE,
                           coded_field="zone_coded",
                           analysis_file_key="zone",
                           fold_strategy=FoldStrategies.assert_label_ids_equal
                       )
                   ],
                   code_imputation_function=code_imputation_functions.impute_somalia_location_codes,
                   ws_code=CodeSchemes.WS_CORRECT_DATASET.get_code_with_match_value("location"),
                   raw_field_fold_strategy=FoldStrategies.assert_equal),

        CodingPlan(raw_field="gender_raw",
                   time_field="gender_time",
                   coda_filename="gender.json",
                   coding_configurations=[
                       CodingConfiguration(
                           coding_mode=CodingModes.SINGLE,
                           code_scheme=CodeSchemes.GENDER,
                           cleaner=somali.DemographicCleaner.clean_gender,
                           coded_field="gender_coded",
                           analysis_file_key="gender",
                           fold_strategy=FoldStrategies.assert_label_ids_equal
                       )
                   ],
                   ws_code=CodeSchemes.WS_CORRECT_DATASET.get_code_with_match_value("gender"),
                   raw_field_fold_strategy=FoldStrategies.assert_equal),

        CodingPlan(raw_field="age_raw",
                   time_field="age_time",
                   coda_filename="age.json",
                   coding_configurations=[
                       CodingConfiguration(
                           coding_mode=CodingModes.SINGLE,
                           code_scheme=CodeSchemes.AGE,
                           cleaner=clean_age_with_range_filter,
                           coded_field="age_coded",
                           analysis_file_key="age",
                           fold_strategy=FoldStrategies.assert_label_ids_equal
                       )
                       # CodingConfiguration(
                       #     coding_mode=CodingModes.SINGLE,
                       #     code_scheme=CodeSchemes.AGE_CATEGORY,
                       #     coded_field="age_category_coded",
                       #     analysis_file_key="age_category",
                       #     fold_strategy=FoldStrategies.assert_label_ids_equal
                       # )
                   ],
                   # code_imputation_function=code_imputation_functions.impute_age_category,
                   ws_code=CodeSchemes.WS_CORRECT_DATASET.get_code_with_match_value("age"),
                   raw_field_fold_strategy=FoldStrategies.assert_equal),

        CodingPlan(raw_field="recently_displaced_raw",
                   time_field="recently_displaced_time",
                   coda_filename="recently_displaced.json",
                   coding_configurations=[
                       CodingConfiguration(
                           coding_mode=CodingModes.SINGLE,
                           code_scheme=CodeSchemes.RECENTLY_DISPLACED,
                           cleaner=somali.DemographicCleaner.clean_yes_no,
                           coded_field="recently_displaced_coded",
                           analysis_file_key="recently_displaced",
                           fold_strategy=FoldStrategies.assert_label_ids_equal
                       )
                   ],
                   ws_code=CodeSchemes.WS_CORRECT_DATASET.get_code_with_match_value("recently displaced"),
                   raw_field_fold_strategy=FoldStrategies.assert_equal),

        CodingPlan(raw_field="in_idp_camp_raw",
                   time_field="in_idp_camp_time",
                   coda_filename="in_idp_camp.json",
                   coding_configurations=[
                       CodingConfiguration(
                           coding_mode=CodingModes.SINGLE,
                           code_scheme=CodeSchemes.IN_IDP_CAMP,
                           cleaner=somali.DemographicCleaner.clean_yes_no,
                           coded_field="in_idp_camp_coded",
                           analysis_file_key="in_idp_camp",
                           fold_strategy=FoldStrategies.assert_label_ids_equal
                       )
                   ],
                   ws_code=CodeSchemes.WS_CORRECT_DATASET.get_code_with_match_value("in idp camp"),
                   raw_field_fold_strategy=FoldStrategies.assert_equal),

        CodingPlan(raw_field="household_language_raw",
                   time_field="household_language_time",
                   coda_filename="household_language.json",
                   coding_configurations=[
                       CodingConfiguration(
                           coding_mode=CodingModes.SINGLE,
                           code_scheme=CodeSchemes.HOUSEHOLD_LANGUAGE,
                           cleaner=None,
                           coded_field="household_language_coded",
                           analysis_file_key="household_language",
                           fold_strategy=FoldStrategies.assert_label_ids_equal
                       )
                   ],
                   ws_code=CodeSchemes.WS_CORRECT_DATASET.get_code_with_match_value("household language"),
                   raw_field_fold_strategy=FoldStrategies.assert_equal),

        CodingPlan(raw_field="government_priority_raw",
                   time_field="government_priority_time",
                   coda_filename="government_priority.json",
                   coding_configurations=[
                       CodingConfiguration(
                           coding_mode=CodingModes.SINGLE,
                           code_scheme=CodeSchemes.GOVERNMENT_PRIORITY,
                           cleaner=None,
                           coded_field="government_priority_coded",
                           analysis_file_key="government_priority",
                           fold_strategy=FoldStrategies.assert_label_ids_equal
                       )
                   ],
                   ws_code=CodeSchemes.WS_CORRECT_DATASET.get_code_with_match_value("s07 government priority"),
                   raw_field_fold_strategy=FoldStrategies.assert_equal)
    ]


def get_ws_correct_dataset_scheme(pipeline_name):
    return CodeSchemes.WS_CORRECT_DATASET
