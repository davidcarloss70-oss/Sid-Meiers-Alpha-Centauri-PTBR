while (True) {
    Write-Host "Iniciando translate_game.py..."
     = Start-Process "uv" -ArgumentList "run","python","translate_game.py" -NoNewWindow -PassThru -Wait
    if (.ExitCode -eq 0) {
        Write-Host "Tradução concluída com sucesso!"
        break
    } else {
        Write-Host "Processo falhou ou travou, reiniciando em 5 segundos..."
        Start-Sleep -Seconds 5
    }
}
