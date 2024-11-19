from source.libs import *
import source.config as config 
import source.preprocessing_functions as pf

# Initialize the FastAPI app
app = FastAPI()

# Mount the static directory to serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Load the dataset
dataframe = pd.read_csv(config.PATH_TO_DATA)
crime_localizer = pf.CrimeLocalizer(dataframe,config.LATITUDE,config.LONGITUDE)

# Create a directory for static files if it doesn't exist
os.makedirs("static", exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def display_home(request: Request):
    unique_districts = dataframe['PdDistrict'].unique().tolist()
    unique_categories = dataframe['Category'].unique().tolist()
    return templates.TemplateResponse("form.html", {
        "request": request, 
        "districts": unique_districts, 
        "categories": unique_categories,
        "map_url": None,
        "chart_url": None,
        "show_results": False
    })

@app.post("/", response_class=HTMLResponse)
async def process_home(request: Request, districts: List[str] = Form(...), categories: List[str] = Form(...), limit: int = Form(1000)):
    filtered_data = crime_localizer.filter_data(districts, categories, limit)
    map_file = crime_localizer.generate_map(filtered_data)
    
    # Serve the static file by referencing its URL path
    map_url = f"/static/{os.path.basename(map_file)}"
    
    unique_districts = dataframe['PdDistrict'].unique().tolist()
    unique_categories = dataframe['Category'].unique().tolist()
    
    return templates.TemplateResponse("form.html", {
        "request": request, 
        "districts": unique_districts, 
        "categories": unique_categories,
        "map_url": map_url,
        "current_districts": districts,
        "current_categories": categories,
        "current_limit": limit
    })
