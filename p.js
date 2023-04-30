
const {google} = require('googleapis');
const key = require('./keys.json');
const client=new google.auth.JWT(
    key.client_email,
    null,
    key.private_key,
    ['https://www.googleapis.com/auth/spreadsheets']

    );
client.authorize(function(err,tokens){
if(err)
{
    console.log(err);
    return;
}else{
    console.log("Connected")
    gsrun(client)
}
});

async function gsrun(cl){
    const gsapi=google.sheets({version:'v4',auth:cl});
    const opt={
      spreadsheetId:'124IzGNQo8rMic181ZCyuE67ZVRkyux4bl6YKHa8k3GY',
      range:'Sheet1!A1:B4'

    };
    let data=await gsapi.spreadsheets.values.get(opt);
    console.log(data.data.values)
}
console.log("dfjkrnvg")
if r==