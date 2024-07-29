def calculate_parabolic_SAR(data, af=0.02, max_af=0.2):
    data['SAR'] = data['Close'].copy()
    data['EP'] = data['Close'].copy()
    data['AF'] = af

    for i in range(1, len(data)):
        if data['Close'].iloc[i] > data['SAR'].iloc[i - 1]:
            data['SAR'].iloc[i] = data['SAR'].iloc[i - 1] + data['AF'].iloc[i - 1] * (data['EP'].iloc[i - 1] - data['SAR'].iloc[i - 1])
            data['EP'].iloc[i] = max(data['EP'].iloc[i - 1], data['Close'].iloc[i])
            data['AF'].iloc[i] = min(data['AF'].iloc[i - 1] + af, max_af)
        else:
            data['SAR'].iloc[i] = data['SAR'].iloc[i - 1] + data['AF'].iloc[i - 1] * (data['EP'].iloc[i - 1] - data['SAR'].iloc[i - 1])
            data['EP'].iloc[i] = min(data['EP'].iloc[i - 1], data['Close'].iloc[i])
            data['AF'].iloc[i] = min(data['AF'].iloc[i - 1] + af, max_af)
    return data['SAR']