import pandas as pd
import plotly.express as px

df = pd.read_csv("../data/rq0_harness_repo.csv", encoding="utf-8")

df['creation date'] = pd.to_datetime(df['creation date'])
df['creation_year'] = df['creation date'].dt.year

year_counts = df['creation_year'].value_counts().sort_values(ascending=False).reset_index()
year_counts.columns = ['Year', 'Count']
year_counts['Year'] = year_counts['Year'].astype(str)

fig = px.bar(
    year_counts,
    x='Year',
    y='Count',
    text='Count',
    color='Count',
    color_continuous_scale='Viridis'
)

fig.update_layout(
    xaxis_title=None,
    yaxis_title='Frequency',
    showlegend=False,
    coloraxis_showscale=False,
    margin=dict(l=0, r=0, t=0, b=0),
    font=dict(size=18),
    xaxis=dict(tickfont=dict(size=18)),
    yaxis=dict(title_font=dict(size=18), tickfont=dict(size=18))
)

fig.update_traces(textposition='outside', textfont_size=18)
fig.write_image("../figures/rq0_creation.pdf")