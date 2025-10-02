$url = 'http://localhost:8080/webhook'

$body = @{
    symbol    = 'BTCUSD'
    timeframe = '1'
    script    = 'POC_TEST'
    signal    = 'BUY'
    price     = 56000.12
    volume    = 2.5
    cvd       = 12345.6
} | ConvertTo-Json -Depth 10

# Send
Invoke-RestMethod -Uri $url -Method Post -Body $body -ContentType 'application/json' | ConvertTo-Json -Depth 10
