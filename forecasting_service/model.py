import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

def get_forecast(forecast_days=14):
    df = pd.read_csv("data.csv")
    df['date'] = pd.to_datetime(df['date'])
    
    # 1. Calculate historical rolling stats
    window = 7
    df['rolling_avg'] = df['value'].rolling(window=window).mean()
    df['std_dev'] = df['value'].rolling(window=window).std()

    # 2. Get the last known values to project forward
    last_date = df['date'].max()
    last_avg = df['rolling_avg'].iloc[-1]
    last_std = df['std_dev'].iloc[-1]

    # 3. Create the "Future" dataframe
    future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=forecast_days)
    future_df = pd.DataFrame({
        'date': future_dates,
        'rolling_avg': [last_avg] * forecast_days, # Naive forecast: future is the last avg
        'std_dev': [last_std] * forecast_days
    })

    # 4. Confidence Bands for Future (95%)
    future_df['upper'] = future_df['rolling_avg'] + (1.96 * future_df['std_dev'])
    future_df['lower'] = future_df['rolling_avg'] - (1.96 * future_df['std_dev'])

    # 5. Combine for visualization
    # We also need CI for the historical part for a clean chart
    df['upper'] = df['rolling_avg'] + (1.96 * df['std_dev'])
    df['lower'] = df['rolling_avg'] - (1.96 * df['std_dev'])
    
    visualize_with_future(df, future_df)
   
    # Save results
    output_file = "forecast_results.csv"
    df.to_csv(output_file, index=False)
    
    # Also save the future projection specifically
    future_df.to_csv("future_only_results.csv", index=False)
    
    print(f"Successfully saved {output_file}")
    print("Successfully saved future_only_results.csv")

def visualize_with_future(df, future_df):
    plt.figure(figsize=(12, 6))
    
    # Plot History
    plt.plot(df['date'], df['value'], label='Historical Actuals', color='black', alpha=0.3)
    plt.plot(df['date'], df['rolling_avg'], label='Historical Trend', color='blue')
    
    # Plot Forecast (Future)
    plt.plot(future_df['date'], future_df['rolling_avg'], label='Forecast', color='red', linestyle='--')
    plt.fill_between(future_df['date'], future_df['lower'], future_df['upper'], 
                     color='red', alpha=0.2, label='Forecast CI (95%)')
    
    plt.axvline(x=df['date'].max(), color='gray', linestyle=':', label='Forecast Start')
    plt.legend()
    plt.title('90-Day History + 14-Day Rolling Forecast')
    plt.savefig('forecast_plot.png')
    plt.show()

if __name__ == "__main__":
    get_forecast()