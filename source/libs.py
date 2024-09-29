import os
import numpy as np
import pandas as pd
import folium
import matplotlib.pyplot as plt
from folium import plugins
import ipywidgets as widgets
from ipywidgets import Layout
from fastapi import FastAPI, Query, Request, Form
from pydantic import BaseModel
from typing import List
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


