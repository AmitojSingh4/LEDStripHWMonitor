const regedit = require('regedit').promisified

async function main() {
    const listResult = await regedit.list('HKCU\\SOFTWARE\\HWiNFO64\\VSB')
    console.log(listResult)
}

main()

//reg query HKEY_CURRENT_USER\SOFTWARE\HWiNFO64\VSB