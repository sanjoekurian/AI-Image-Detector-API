# AI-Image-Detector-API
This is a Fastapi Based API used to detect whether a given image is AI generated or not.Just Install the requirements,collect one API key from the sightengine website run the server and you are good to go.
Clone the repository and create a .env file.Get the API key and API user code from the sightengine Webisite.Save it in the format as below
API_USER=<Your API User Code here>
API_SECRET=<Your Secret API key here>

Install the dependencies using the script pip install requirements.txt.
After Successful Installation,run the FastAPI server with 
uvicorn main:app --reload

Two mode of input can be given to the system-one is using the image URL and other is direct uploading of the image.
