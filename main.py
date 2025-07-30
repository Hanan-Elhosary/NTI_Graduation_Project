from fastapi import FastAPI, Request, Form  ,File, UploadFile
from fastapi.responses import HTMLResponse , RedirectResponse
from fastapi.templating import Jinja2Templates
import pandas as pd
import plotly.express as px
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")
UPLOAD_DIR = "uploads"
UPLOADED_FILE_PATH = os.path.join(UPLOAD_DIR, "data.csv")
os.makedirs(UPLOAD_DIR, exist_ok=True)



@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})



@app.post("/upload", response_class=HTMLResponse)
async def upload_file(request: Request, file: UploadFile = File(...)):
    contents = await file.read()

    # حفظ الملف في المسار المناسب
    with open(UPLOADED_FILE_PATH, "wb") as f:
        f.write(contents)

    # بعد الرفع، نرجّع المستخدم لصفحة اختيار العمود
    df = pd.read_csv(UPLOADED_FILE_PATH)
    columns = df.columns.tolist()

    return templates.TemplateResponse("choose_column.html", {
        "request": request,
        "columns": columns
    })

@app.post("/plot", response_class=HTMLResponse)
async def generate_plot(request: Request, column: str = Form(...)):
    try:
        df = pd.read_csv(UPLOADED_FILE_PATH)

        # لو العمود موجود نرسمه
        if column in df.columns:
            fig = px.histogram(df, x=column)
            plot_html = fig.to_html(full_html=False)
        else:
            plot_html = "<p>العمود غير موجود في البيانات.</p>"

        return templates.TemplateResponse("visualize_result.html", {
            "request": request,
            "plot_html": plot_html
        })
    except Exception as e:
        return templates.TemplateResponse("visualize_result.html", {
            "request": request,
            "plot_html": f"<p>حدث خطأ: {str(e)}</p>"
        })
