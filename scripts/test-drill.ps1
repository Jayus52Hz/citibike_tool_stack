$ErrorActionPreference = "Stop"

$query = 'SELECT columns[0] AS id, columns[1] AS name, columns[2] AS value FROM dfs.`/sample-data/test.csv` WHERE columns[0] <> ''id'''
$body = @{
  queryType = "SQL"
  query = $query
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:8047/query.json" -Method Post -ContentType "application/json" -Body $body
$response | ConvertTo-Json -Depth 10
