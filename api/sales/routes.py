from api import app
from api.sales import views


@app.route('/purchases', methods=["GET", "POST"], strict_slashes=False)
def purchases():
    return views.purchase_view()
