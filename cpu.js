const regedit = require('regedit').promisified

async function getData() {
    return await regedit.list('HKCU\\SOFTWARE\\HWiNFO64\\VSB')
}

Bun.serve({
    async fetch(req) {
        return Response.json(await getData());
    },
});

//reg query HKEY_CURRENT_USER\SOFTWARE\HWiNFO64\VSB
//http://localhost:3000/