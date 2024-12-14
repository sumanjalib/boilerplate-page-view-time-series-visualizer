import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# 1. Import data
df = pd.read_csv('fcc-forum-pageviews.csv', index_col='date', parse_dates=['date'])

# 2. Clean the data
df = df[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]


# 3. Line Plot
def draw_line_plot():
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df.index, df['value'], color='r', linewidth=1)

    # Add title and labels
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')

    # Save figure
    fig.savefig('line_plot.png')
    return fig


# 4. Bar Plot
def draw_bar_plot():
    # Prepare data for bar plot
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month_name()

    # Group by year and month to calculate the mean
    df_bar = df_bar.groupby(['year', 'month'], sort=False)['value'].mean().reset_index()
    df_bar['month'] = pd.Categorical(df_bar['month'], categories=[
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ], ordered=True)

    # Pivot table for plotting
    df_pivot = df_bar.pivot(index='year', columns='month', values='value')

    # Draw bar plot
    fig, ax = plt.subplots(figsize=(12, 6))
    df_pivot.plot(kind='bar', ax=ax)
    
    # Add labels and title
    ax.set_title('Average Daily Page Views per Month')
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    ax.legend(title='Months', fontsize=8)
    ax.set_xticks(range(len(df_pivot.index)))
    ax.set_xticklabels(df_pivot.index, rotation=45)

    # Save figure
    fig.savefig('bar_plot.png')
    return fig


# 5. Box Plot
def draw_box_plot():
    # Prepare data for box plots
    df_box = df.copy()
    df_box['year'] = df_box.index.year
    df_box['month'] = df_box.index.month_name()
    df_box['month_num'] = df_box.index.month
    df_box.sort_values('month_num', inplace=True)

    # Draw box plots
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(15, 6))

    # Year-wise Box Plot
    sns.boxplot(
        x='year',
        y='value',
        data=df_box,
        ax=axes[0]
    )
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')

    # Month-wise Box Plot
    sns.boxplot(
        x='month',
        y='value',
        data=df_box,
        ax=axes[1]
    )
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')
    axes[1].tick_params(axis='x', rotation=45)

    # Save figure
    fig.savefig('box_plot.png')
    return fig
