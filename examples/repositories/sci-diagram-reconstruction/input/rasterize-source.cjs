const sharp = require(process.argv[2]);
sharp(process.argv[3]).png().toFile(process.argv[4]);
