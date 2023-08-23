import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("fcc-forum-pageviews.csv",parse_dates=["date"]) #parse' converts the data from date to a date format
df.set_index('date', inplace=True) 
# Clean data taking out the upper and bottom 2.5% 
top_threshold = df['value'].quantile(0.975) #with quantile function you can select that direct value which results from calculatuing an exact position after sortering it, is faster
bottom_threshold = df['value'].quantile(0.025)

# Create masks for days exceeding the top threshold or falling below the bottom threshold
mask_top = df['value'] > top_threshold
mask_bottom = df['value'] < bottom_threshold

# Apply masks to filter out the rows
df = df[~(mask_top | mask_bottom)] #df filter all not in ~ OR /


def draw_line_plot():
    # Draw line plot, fig is gonna be the png later and ax is like the object itself, the maths to later draw 
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot the data as a line chart
    # first two are the axes, then color, then the grosor de la linea y then el name of what the line represents, this is shown in the legend
    ax.plot(df.index, df['value'], color='r', linewidth=1, label='Page Views') 
    
    # Set labels and title
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    
    # Format the date ticks on the x-axis
    ax.xaxis.set_major_locator(plt.MaxNLocator(8))  # Show a maximum of 8 ticks on x axis
    plt.xticks(rotation=45) # this rotates 45degrees the labels under the ticks for nicer view
    
    # Add legend
    ax.legend(loc='upper left')
    
    # Save image and return fig
    fig.savefig('line_plot.png')
    return fig


def draw_bar_plot(): 
    df_bar = df.copy() 
    
    # Extract the year from the date and adding that column
    df_bar['year'] = df_bar.index.year

    # Convert the month number from date to month name
    df_bar['month'] = df_bar.index.strftime('%B') #this names the number of month as a streing with its correspondant name
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    df_bar['month'] = pd.Categorical(df_bar['month'], categories=month_order, ordered=True) #sorting months under the categorical fc from pandas

    # Group by year and month and calculate the average per month
    df_grouped = df_bar.groupby(['year', 'month']).mean()
    
    # Reset index for plotting (this should be always done)
    df_grouped = df_grouped.reset_index()
    
    # Draw bar plot
    plt.figure(figsize=(10, 10))

    unique_months = df_grouped['month'].unique()
    sns.barplot(x='year', y='value', hue='month', #hue is like the categorie that you are grouping
                 data=df_grouped, width=0.3, #data coming from dfgrouped and the width setted
                palette=sns.color_palette("Set1", n_colors=len(unique_months)))  # Set palette with unique colors
    plt.xticks(rotation=45)
    plt.xlabel('Years') #naming labels
    plt.ylabel('Average Page Views')
    plt.title('Average Daily Page Views for Each Month Grouped by Year')
    
    # Customize the legend
    plt.legend(loc = 'upper left')
    
    # Save image and return fig (don't change this part)
    plt.tight_layout() # this makes sure that nothing is crashing visually or superposed
    fig = plt.gcf() #get current figure, this gets the object itself that was being made and puts it into fig
    fig.savefig('bar_plot.png') #we name the file of fig as a png.
    return fig #we return it

# Call the function to draw the bar plot and save the figure
draw_bar_plot()

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)





    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
