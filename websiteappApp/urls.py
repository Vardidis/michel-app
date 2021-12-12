from django.urls import path
from . import views

urlpatterns = [
	path("", views.index, name="index"),
	path("trades/", views.trades, name="trades"),
	path("account/", views.account, name="account"),
	path("api/getAllPairs", views.getAllPairs),
	path('api/<str:coin>/<str:pair>/<int:price>/<int:dec>/<int:amount>/<int:dec2>/<str:event>', views.postOrder),
	path('api/getBalance/', views.getBalance),
	path('api/fetchTable/', views.fetchTable),
	path('api/deleteFromTable/<int:id>/', views.removeTable),
	path('api/fetchOpenOrders/', views.fetchOpenOrders),
	path('api/deleteOpenOrders/<int:id>/', views.removeOrders),
	path('api/addFav/<str:coin>/<str:pair>', views.addFav),
	path('api/updateBalance/<int:tot>/<int:tal>/<str:event>', views.updateBalance),
	path('api/checkPortfolio/<int:tot>/<int:tal>/<str:coin>/<str:pair>', views.checkPortfolio),
	path('api/fetchPortfolio/', views.fetchPortfolio),
	path('api/fetchHistory', views.fetchHistory),
]