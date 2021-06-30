import dash

# meta_tags are required for the app layout to be mobile responsive
bs = "https://stackpath.bootstrapcdn.com/bootswatch/4.5.2/darkly/bootstrap.min.css"

app = dash.Dash(__name__,external_stylesheets=[bs], meta_tags = [{"name": "viewport", "content": "width=device-width"}])

server=app.server