# columns.py

# Define the columns to be used across different queries
COMMON_COLUMNS = [
    "applicant_id", "adhaar_number", "first_name", "last_name", "middle_name", "mobile_number",
    "email", "date_of_birth", "gender", "age", "caste", "your_caste", "subcaste", "pvtg",
    "pvtg_caste", "marital_status", "dependents", "state", "district", "taluka", "village",
    "city", "add_1", "add_2", "pincode", "ssc_passing_year", "ssc_percentage", "ssc_school_name",
    "ssc_stream", "ssc_attempts", "ssc_total", "hsc_passing_year", "hsc_percentage", "hsc_school_name",
    "hsc_stream", "hsc_attempts", "hsc_total", "graduation_passing_year", "graduation_percentage",
    "graduation_school_name", "grad_stream", "grad_attempts", "grad_total", "phd_passing_year",
    "phd_percentage", "phd_school_name", "pg_stream", "pg_attempts", "pg_total", "have_you_qualified",
    "name_of_college", "other_college_name", "name_of_guide", "topic_of_phd", "concerned_university",
    "department_name", "faculty", "phd_registration_date", "phd_registration_year", "phd_registration_age",
    "family_annual_income", "income_certificate_number", "issuing_authority", "income_issuing_district",
    "income_issuing_taluka", "domicile", "domicile_certificate", "domicile_number", "validity_certificate",
    "validity_cert_number", "validity_issuing_district", "validity_issuing_taluka", "validity_issuing_authority",
    "caste_certf", "caste_certf_number", "issuing_district", "caste_issuing_authority", "salaried", "disability",
    "type_of_disability", "father_name", "mother_name", "work_in_government", "gov_department", "gov_position",
    "bank_name", "account_number", "ifsc_code", "account_holder_name", "micr"
]


# Define the headers as a dictionary
COMMON_HEADERS = {
    "applicant_id": "Applicant ID",
    "adhaar_number": "Aadhaar Number",
    "first_name": "First Name",
    "last_name": "Last Name",
    "middle_name": "Middle Name",
    "mobile_number": "Mobile Number",
    "email": "Email",
    "date_of_birth": "Date of Birth",
    "gender": "Gender",
    "age": "Age",
    "caste": "Caste",
    "your_caste": "Your Caste",
    "subcaste": "Subcaste",
    "pvtg": "PVTG",
    "pvtg_caste": "PVTG Caste",
    "marital_status": "Marital Status",
    "dependents": "Dependents",
    "state": "State",
    "district": "District",
    "taluka": "Taluka",
    "village": "Village",
    "city": "City",
    "add_1": "Address Line 1",
    "add_2": "Address Line 2",
    "pincode": "Pincode",
    "ssc_passing_year": "SSC Passing Year",
    "ssc_percentage": "SSC Percentage",
    "ssc_school_name": "SSC School Name",
    "ssc_stream": "SSC Stream",
    "ssc_attempts": "SSC Attempts",
    "ssc_total": "SSC Total",
    "hsc_passing_year": "HSC Passing Year",
    "hsc_percentage": "HSC Percentage",
    "hsc_school_name": "HSC School Name",
    "hsc_stream": "HSC Stream",
    "hsc_attempts": "HSC Attempts",
    "hsc_total": "HSC Total",
    "graduation_passing_year": "Graduation Passing Year",
    "graduation_percentage": "Graduation Percentage",
    "graduation_school_name": "Graduation School Name",
    "grad_stream": "Graduation Stream",
    "grad_attempts": "Graduation Attempts",
    "grad_total": "Graduation Total",
    "phd_passing_year": "PhD Passing Year",
    "phd_percentage": "PhD Percentage",
    "phd_school_name": "PhD School Name",
    "pg_stream": "PG Stream",
    "pg_attempts": "PG Attempts",
    "pg_total": "PG Total",
    "have_you_qualified": "Have You Qualified",
    "name_of_college": "Name of College",
    "other_college_name": "Other College Name",
    "name_of_guide": "Name of Guide",
    "topic_of_phd": "Topic of PhD",
    "concerned_university": "Concerned University",
    "department_name": "Department Name",
    "faculty": "Faculty",
    "phd_registration_date": "PhD Registration Date",
    "phd_registration_year": "PhD Registration Year",
    "phd_registration_age": "PhD Registration Age",
    "family_annual_income": "Family Annual Income",
    "income_certificate_number": "Income Certificate Number",
    "issuing_authority": "Issuing Authority",
    "income_issuing_district": "Income Issuing District",
    "income_issuing_taluka": "Income Issuing Taluka",
    "domicile": "Domicile",
    "domicile_certificate": "Domicile Certificate",
    "domicile_number": "Domicile Number",
    "validity_certificate": "Validity Certificate",
    "validity_cert_number": "Validity Certificate Number",
    "validity_issuing_district": "Validity Issuing District",
    "validity_issuing_taluka": "Validity Issuing Taluka",
    "validity_issuing_authority": "Validity Issuing Authority",
    "caste_certf": "Caste Certificate",
    "caste_certf_number": "Caste Certificate Number",
    "issuing_district": "Issuing District",
    "caste_issuing_authority": "Caste Issuing Authority",
    "salaried": "Salaried",
    "disability": "Disability",
    "type_of_disability": "Type of Disability",
    "father_name": "Father's Name",
    "mother_name": "Mother's Name",
    "work_in_government": "Work in Government",
    "gov_department": "Government Department",
    "gov_position": "Government Position",
    "bank_name": "Bank Name",
    "account_number": "Account Number",
    "ifsc_code": "IFSC Code",
    "account_holder_name": "Account Holder Name",
    "micr": "MICR"
}

