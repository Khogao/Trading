$names = @('PI-03.pine', 'PI-04.pine', 'PI-05.pine', 'PI-17.pine')
foreach ($n in $names) {
    $found = Get-ChildItem -Path . -Recurse -Filter $n -File -ErrorAction SilentlyContinue
    if ($found) {
        $found | ForEach-Object { Write-Output "FOUND|$($_.FullName)" }
    }
    else {
        Write-Output "NOTFOUND|$n"
    }
}
