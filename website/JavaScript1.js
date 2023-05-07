// Load the Google Sheets API client library
gapi.load('client', start);

// Initialize the Google Sheets API client library
function start() {
    gapi.client.init({
        apiKey: 'YOUR_API_KEY',
        discoveryDocs: ['https://sheets.googleapis.com/$discovery/rest?version=v4'],
        clientId: 'YOUR_CLIENT_ID',
        scope: 'https://www.googleapis.com/auth/spreadsheets.readonly'
    }).then(getPredictions);
}

// Retrieve the data from the Google spreadsheet
function getPredictions() {
    gapi.client.sheets.spreadsheets.values.get({
        spreadsheetId: 'YOUR_SPREADSHEET_ID',
        range: 'Round 1!A1:C10'
    }).then(function (response) {
        var values = response.result.values;
        var predictionsElement = document.getElementById('predictions');
        for (var i = 0; i < values.length; i++) {
            var team = values[i][0];
            var gameNumber = values[i][1];
            var prediction = values[i][2];
            var card = document.createElement('div');
            card.className = 'card';
            card
