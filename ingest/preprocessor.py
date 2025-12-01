def build_features(window=3):
    df = load_events()
    # rolling stats
    f = pd.DataFrame(index=df.index)
    f['latency_mean'] = df['latency_p95'].rolling(window).mean().bfill()  # changed here
    f['latency_std'] = df['latency_p95'].rolling(window).std().fillna(0)
    f['err_mean'] = df['error_rate'].rolling(window).mean().fillna(0)
    f['lag_mean'] = df['kafka_consumer_lag'].rolling(window).mean().fillna(0)
    # latest values
    f['latency_now'] = df['latency_p95']
    f['err_now'] = df['error_rate']
    f['lag_now'] = df['kafka_consumer_lag']
    f = f.fillna(0)
    f.to_csv(os.path.join(os.path.dirname(__file__), '..', 'data', 'features.csv'))
    print("Features written to data/features.csv")
    return f
