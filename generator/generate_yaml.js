var apiconnWsdl = require("apiconnect-wsdl");
var yaml = require("js-yaml");
var fs = require("fs");

var EXTENSION = ".wsdl";
var wsdlFiles = [];
var wsdlFilesP = [];

//requiring path and fs modules
const path = require("path");

//joining path of directory
const directoryPath = path.join(__dirname, "src/wsdl");

const filenames = fs.readdirSync(directoryPath);

console.log("\nCurrent directory filenames:");
filenames.forEach((file) => {
  if (path.extname(file).toLowerCase() === EXTENSION) {
    console.log(`Found file : ${file}`);
    wsdlFiles.push(file);

    try {
      wsdlFilesP.push(
        apiconnWsdl.getJsonForWSDL(`${__dirname}/src/wsdl/${file}`)
      );
    } catch (err) {
      console.log(`Errore !!!!!!! ${err}`);
    }
  }
});

// get WSDL files
// var promise = apiconnWsdl.getJsonForWSDL(
//   `${__dirname}/src/wsdl/pspForNode.wsdl`
// );

console.log("Starting then promise...");

// call genereate WSDL_2_YAML
wsdlFilesP.forEach((e) =>
  e.then(
    function (wsdls) {
      // Get Services from all parsed WSDLs
      var serviceData = apiconnWsdl.getWSDLServices(wsdls);

      // Loop through all services and genereate yaml file
      for (var item in serviceData.services) {
        var serviceName = serviceData.services[item].service;
        var wsdlId = serviceData.services[item].filename;
        var wsdlEntry = apiconnWsdl.findWSDLForServiceName(wsdls, serviceName);
        var swagger = apiconnWsdl.getSwaggerForService(
          wsdlEntry,
          serviceName,
          wsdlId
        );
        fs.writeFileSync(
          `${__dirname}/out/${serviceName}.yaml`,
          yaml.safeDump(swagger)
        );
        console.log(`Generated ${serviceName}.yaml ... DONE!`);
      }
    },
    function (error) {
      console.log("Errore..........");
      console.log(error.message);
    }
  )
);

// promise.then(
//   function (wsdls) {
//     // Get Services from all parsed WSDLs
//     var serviceData = apiconnWsdl.getWSDLServices(wsdls);

//     // Loop through all services and genereate yaml file
//     for (var item in serviceData.services) {
//       var serviceName = serviceData.services[item].service;
//       var wsdlId = serviceData.services[item].filename;
//       var wsdlEntry = apiconnWsdl.findWSDLForServiceName(wsdls, serviceName);
//       var swagger = apiconnWsdl.getSwaggerForService(
//         wsdlEntry,
//         serviceName,
//         wsdlId
//       );
//       fs.writeFileSync(
//         `${__dirname}/out/${serviceName}.yaml`,
//         yaml.safeDump(swagger)
//       );
//       console.log(`Generated ${serviceName}.yaml ... DONE!`);
//     }
//   },
//   function (error) {
//     console.log("Errore..........");
//     console.log(error.message);
//   }
// );
