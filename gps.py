def plot_route(data):
  f= open(".mapbox_token.txt","w+")
  f.write("pk.eyJ1Ijoiam9ub2NodXJjaCIsImEiOiJja3VuZjQzbjEyNTNyMm5vZnF4cWNnbjR5In0.EtsN55_VNAPh07GqeWUgcA")
  f.close()
  px.set_mapbox_access_token(open(".mapbox_token.txt").read())

  fig = px.scatter_mapbox(data, lat="Lat", lon="Lon",     
                    mapbox_style='satellite', zoom=14, width=700, height=350,
                    )
  fig.update_traces(#mode='lines',
                    marker=dict(
                        size=5,
          color=(df['Speed']*3.6), #set color equal to a variable
          colorscale='Turbo', # one of plotly colorscales
          showscale=True))
  fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
  fig.show()
  fig=px.scatter(data, x=data.index, y='Speed',
                width=500, height=150 
                )
  fig.update_traces(mode='lines',
                    marker=dict(
                        size=5,))
  fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

  return fig.show()
