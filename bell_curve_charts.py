import numpy as np
import plotly.graph_objects as go

def create_bell_curve_chart(df, mean, std_dev):
    # Generate data for the bell curve
    x = np.linspace(mean - 3*std_dev, mean + 3*std_dev, 100)
    y = (1 / (std_dev * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mean) / std_dev) ** 2)

    # Calculate the density of the bell curve at the data points
    density_at_points = (1 / (std_dev * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((df['Final'] - mean) / std_dev) ** 2)

    # Ensure points are placed within the density range and do not overlap vertically
    points_with_jitter = []
    for i in range(len(df)):
        while True:
            jitter = np.random.uniform(-20 * std_dev, 20 * std_dev)  # Increased jitter range for better separation
            new_y = density_at_points[i] - jitter  # Ensure points are under the curve
            if 0 <= new_y <= density_at_points[i]:
                points_with_jitter.append((df['Final'][i], new_y))
                break

    jittered_x, jittered_y = zip(*points_with_jitter) if points_with_jitter else ([], [])

    # Sort the DataFrame by 'Final' to identify the top 3 points
    df_sorted = df.sort_values(by='Final', ascending=False)
    top_3_indices = df_sorted.head(3).index

    # Color data points: top 3 green, rest red
    colors = ['green' if i in top_3_indices else 'red' for i in df.index]

    # Create the bell curve plot
    bell_curve = go.Scatter(
        x=x,
        y=y,
        mode='lines',
        name='Bell Curve',
        line=dict(color='blue')
    )

    # Create a mean point for the legend
    mean_point = go.Scatter(
        x=[mean],
        y=[(1 / (std_dev * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((mean - mean) / std_dev) ** 2)],
        mode='markers',
        name=f'Mean: {mean:.2f}',
        marker=dict(color='black', size=12, symbol='cross')
    )

    # Create the data points plot with category names as text
    data_points = go.Scatter(
        x=jittered_x,
        y=jittered_y,  # Use adjusted y-values
        mode='markers+text',
        name='Data Points',
        marker=dict(color=colors, size=10),
        text=df['Fund'],
        textposition='top center'
    )

    # Create shaded areas for standard deviations
    shading = []
    shading_colors = ['rgba(0, 0, 255, 0.2)', 'rgba(0, 255, 0, 0.2)', 'rgba(255, 0, 0, 0.2)']
    ranges = [
        (mean - 3*std_dev, mean + 3*std_dev),  # 3σ
        (mean - 2*std_dev, mean + 2*std_dev),  # 2σ
        (mean - std_dev, mean + std_dev)       # 1σ
    ]

    for i, (range_start, range_end) in enumerate(ranges):
        shading.append(go.Scatter(
            x=[range_start, range_end, range_end, range_start],
            y=[0, 0, max(y), max(y)],
            fill='toself',
            fillcolor=shading_colors[i],
            line=dict(color='rgba(255,255,255,0)'),
            showlegend=False
        ))

    # Create vertical lines for standard deviations
    vertical_lines = [
        mean - 3*std_dev, mean - 2*std_dev, mean - std_dev,
        mean + std_dev, mean + 2*std_dev, mean + 3*std_dev
    ]
    lines = [go.Scatter(
        x=[line, line],
        y=[0, max(y)],
        mode='lines',
        line=dict(color='black', dash='dash'),
        name=f'{int(abs(mean - line)/std_dev)}σ' if line != mean else f'Mean: {mean:.2f}'
    ) for line in vertical_lines]

    # Combine all plots into a figure
    fig = go.Figure(data=[bell_curve, data_points, mean_point] + shading + lines)

    # Update layout
    fig.update_layout(
        title='Bell Curve with Standard Deviations and Categories',
        xaxis_title='Final Average',
        yaxis_title='Probability Density',
        showlegend=True
    )

    return fig
