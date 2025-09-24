(venv) PS C:\Users\user\Desktop\Phase10_BLR_visit_19092025\Srinivas-Sep-23\GenAI\langchain>
(venv) PS C:\Users\user\Desktop\Phase10_BLR_visit_19092025\Srinivas-Sep-23\GenAI\langchain> python .\resume_extractor.py --pdf .\Alexander_Resume_ML_DL_DS.pdf --output "resume_output.json"

{
    "Name": "Alexander Reddy",
    "Email": "alexvatti@gmail.com",
    "Phone": "9566177461",
    "Education": "National Institute of Technology, Warangal, India. Jun 20 04",
    "Experience": [
        {
            "JobTitle": "Machine Learning Engineer",
            "Company": "Qvantel",
            "Location": "Hyderabad",
            "Duration": "March 2020 \u2013 Oct 2023",
            "Responsibilities": [
                "Developed advanced functionalities for the Algro IVD smart camera, focusing on precise barcode decoding, accurate liquid level measurement, and deep learning-based cap detection.",
                "Ensured robust performance in IVD applications, enhancing sample tracking, analytical precision, and quality control in medical environments."
            ]
        }
    ],
    "Skills": [
        "Programming",
        "Data Manipulation",
        "Analysis",
        "Data Visualization",
        "Machine Learning",
        "Deep Learning",
        "Natural Language Processing (NLP)",
        "Image Processing",
        "Deployment",
        "Cloud",
        "Python",
        "Pandas",
        "Matplotlib",
        "Scikit-learn",
        "TensorFlow/Keras",
        "NLTK",
        "OpenCV",
        "Flask",
        "AWS",
        "SQL",
        "NumPy",
        "Seaborn",
        "XGBoost",
        "PyTorch",
        "SpaCy",
        "Pillow",
        "Streamlit",
        "Azure"
    ]
}

✅ Saved JSON to resume_output.json
(venv) PS C:\Users\user\Desktop\Phase10_BLR_visit_19092025\Srinivas-Sep-23\GenAI\langchain> cd .\Streamlit-GenAI-Apps\
(venv) PS C:\Users\user\Desktop\Phase10_BLR_visit_19092025\Srinivas-Sep-23\GenAI\langchain\Streamlit-GenAI-Apps>  python -m streamlit run .\resume_extractor_st.py

  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.0.105:8501

