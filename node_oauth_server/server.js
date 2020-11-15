const http = require('http');
const https = require('https');
const url = require('url');

const hostname = '127.0.0.1';
const port = 4242;

const app_id = '';
const permissions = 'manage_library,offline_access';
const secret_key = '';
const redirect_url = 'http://ec2-35-178-91-53.eu-west-2.compute.amazonaws.com/redirect';

const login_page = '<html><form action="http://ec2-35-178-91-53.eu-west-2.compute.amazonaws.com/connect"><input type="submit" value="Connect to Deezer" /></form></html>';

let token = null;

const server = http.createServer((req, res) => {
  console.log(`got request on ${req.url}`);
  const parsed_url = url.parse(req.url, true);
  if (parsed_url.pathname === '/redirect') {
    const deezer_code = parsed_url.query.code;
    const access_token_url = `https://connect.deezer.com/oauth/access_token.php?app_id=${app_id}&secret=${secret_key}&code=${deezer_code}&output=json`
    console.log(`url = ${access_token_url}`);
    https.get(access_token_url, (resp) => {
      let data = '';
      resp.on('data', (chunk) => {
        data += chunk;
      });
      resp.on('end', () => {
        console.log(`data = ${data}`);
        token = JSON.parse(data);
        console.log(token);
      });
    }).on("error", (err) => {
      console.log(`err = ${err.message}`);
    });
    res.statusCode = 200;
    res.end();
  }
  else if (parsed_url.pathname === '/') {
    res.statusCode = 200;
    res.end(login_page);
  }
  else if (parsed_url.pathname === '/connect') {
    res.writeHead(301, {Location: `https://connect.deezer.com/oauth/auth.php?app_id=${app_id}&redirect_uri=${redirect_url}&perms=${permissions}`});
    res.end();
  }
});

server.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});

