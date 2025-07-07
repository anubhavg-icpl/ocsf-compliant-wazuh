import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# Data from the provided JSON
data = {
    "time": ["2024-07-07T00:00:00", "2024-07-07T01:00:00", "2024-07-07T02:00:00", "2024-07-07T03:00:00", "2024-07-07T04:00:00", "2024-07-07T05:00:00", "2024-07-07T06:00:00", "2024-07-07T07:00:00", "2024-07-07T08:00:00", "2024-07-07T09:00:00", "2024-07-07T10:00:00", "2024-07-07T11:00:00", "2024-07-07T12:00:00", "2024-07-07T13:00:00", "2024-07-07T14:00:00", "2024-07-07T15:00:00", "2024-07-07T16:00:00", "2024-07-07T17:00:00", "2024-07-07T18:00:00", "2024-07-07T19:00:00", "2024-07-07T20:00:00", "2024-07-07T21:00:00", "2024-07-07T22:00:00", "2024-07-07T23:00:00"],
    "throughput_eps": [125, 98, 87, 78, 82, 95, 145, 234, 456, 678, 743, 821, 892, 934, 876, 823, 756, 645, 432, 298, 234, 187, 156, 134],
    "latency_p50": [23, 18, 16, 14, 15, 19, 28, 35, 45, 52, 58, 62, 68, 71, 66, 61, 54, 47, 38, 31, 28, 24, 21, 20],
    "latency_p95": [78, 65, 58, 52, 56, 67, 89, 112, 145, 168, 182, 198, 215, 228, 221, 204, 186, 162, 134, 108, 97, 86, 76, 72],
    "latency_p99": [156, 132, 118, 108, 115, 138, 178, 225, 289, 335, 364, 396, 430, 456, 442, 408, 372, 324, 268, 216, 194, 172, 152, 144],
    "error_rate": [0.1, 0.08, 0.06, 0.05, 0.07, 0.12, 0.18, 0.25, 0.35, 0.42, 0.38, 0.41, 0.45, 0.48, 0.44, 0.39, 0.33, 0.28, 0.22, 0.16, 0.13, 0.11, 0.09, 0.08],
    "memory_usage_mb": [1024, 985, 932, 889, 908, 976, 1187, 1456, 1789, 2234, 2456, 2678, 2891, 3012, 2867, 2634, 2398, 2156, 1834, 1567, 1298, 1187, 1098, 1045],
    "queue_depth": [12, 8, 6, 4, 5, 9, 18, 28, 45, 67, 78, 89, 94, 98, 91, 82, 73, 62, 48, 32, 24, 19, 15, 13]
}

# Convert to DataFrame
df = pd.DataFrame(data)
df['time'] = pd.to_datetime(df['time'])

# Convert memory from MB to GB for better scale
df['memory_usage_gb'] = df['memory_usage_mb'] / 1024

# Create figure focusing on throughput as primary metric
fig = go.Figure()

# Add throughput as primary metric
fig.add_trace(go.Scatter(
    x=df['time'],
    y=df['throughput_eps'],
    mode='lines+markers',
    name='Throughput',
    line=dict(color='#1FB8CD', width=4),
    marker=dict(size=6),
    hovertemplate='<b>%{x}</b><br>Throughput: %{y} EPS<br>P50 Latency: %{customdata[0]}ms<br>P95 Latency: %{customdata[1]}ms<br>Error Rate: %{customdata[2]}%<br>Memory: %{customdata[3]:.1f}GB<br>Queue Depth: %{customdata[4]}<extra></extra>',
    customdata=list(zip(df['latency_p50'], df['latency_p95'], df['error_rate'], df['memory_usage_gb'], df['queue_depth'])),
    cliponaxis=False
))

# Add area fill to show throughput pattern
fig.add_trace(go.Scatter(
    x=df['time'],
    y=df['throughput_eps'],
    mode='lines',
    name='Throughput Area',
    line=dict(color='#1FB8CD', width=0),
    fill='tozeroy',
    fillcolor='rgba(31, 184, 205, 0.2)',
    showlegend=False,
    hoverinfo='skip',
    cliponaxis=False
))

# Add queue depth as secondary indicator scaled to throughput range
queue_scale = df['throughput_eps'].max() / df['queue_depth'].max()
df['queue_scaled'] = df['queue_depth'] * queue_scale

fig.add_trace(go.Scatter(
    x=df['time'],
    y=df['queue_scaled'],
    mode='lines',
    name='Queue Depth',
    line=dict(color='#D2BA4C', width=2, dash='dash'),
    marker=dict(size=4),
    hovertemplate='<b>%{x}</b><br>Queue Depth: %{customdata}<extra></extra>',
    customdata=df['queue_depth'],
    cliponaxis=False
))

# Update layout
fig.update_layout(
    title='Pipeline Performance Dashboard',
    xaxis_title='Time',
    yaxis_title='Events/Second',
    legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='center', x=0.5)
)

# Update axes
fig.update_xaxes(showgrid=True)
fig.update_yaxes(showgrid=True, range=[0, df['throughput_eps'].max() * 1.1])

# Save as PNG
fig.write_image("pipeline_performance.png")