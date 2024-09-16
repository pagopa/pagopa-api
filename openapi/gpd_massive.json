{
  "openapi": "3.0.1",
  "info": {
    "title": "pagopa-gpd-upload",
    "version": "0.1.17"
  },
  "paths": {
    "/brokers/{broker-code}/organizations/{organization-fiscal-code}/debtpositions/file": {
      "put": {
        "tags": [
          "Debt Positions CRUD via file upload API"
        ],
        "summary": "The Organization updates the debt positions listed in the file.",
        "operationId": "update-debt-positions-by-file-upload",
        "parameters": [
          {
            "name": "broker-code",
            "in": "path",
            "description": "The broker code",
            "required": true,
            "schema": {
              "minLength": 1,
              "type": "string"
            }
          },
          {
            "name": "organization-fiscal-code",
            "in": "path",
            "description": "The organization fiscal code",
            "required": true,
            "schema": {
              "minLength": 1,
              "type": "string"
            }
          }
        ],
        "requestBody": {
          "content": {
            "multipart/form-data": {
              "schema": {
                "type": "object",
                "properties": {
                  "file": {
                    "type": "string",
                    "description": "File to be uploaded",
                    "format": "binary"
                  }
                }
              },
              "encoding": {
                "file": {
                  "contentType": "application/octet-stream"
                }
              }
            }
          },
          "required": true
        },
        "responses": {
          "202": {
            "description": "Request accepted."
          },
          "400": {
            "description": "Malformed request.",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/ProblemJson"
                }
              }
            }
          },
          "401": {
            "description": "Wrong or missing function key.",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/ProblemJson"
                }
              }
            }
          },
          "403": {
            "description": "Forbidden",
            "content": {
              "application/json": {
                "schema": {
                  "allOf": [],
                  "anyOf": [],
                  "oneOf": []
                }
              }
            }
          },
          "409": {
            "description": "Conflict: duplicate file found.",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/ProblemJson"
                }
              }
            }
          },
          "429": {
            "description": "Too many requests.",
            "content": {
              "text/json": {}
            }
          },
          "500": {
            "description": "Service unavailable.",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/ProblemJson"
                }
              }
            }
          }
        }
      },
      "post": {
        "tags": [
          "Debt Positions CRUD via file upload API"
        ],
        "summary": "The Organization creates the debt positions listed in the file.",
        "operationId": "create-debt-positions-by-file-upload",
        "parameters": [
          {
            "name": "broker-code",
            "in": "path",
            "description": "The broker code",
            "required": true,
            "schema": {
              "minLength": 1,
              "type": "string"
            }
          },
          {
            "name": "organization-fiscal-code",
            "in": "path",
            "description": "The organization fiscal code",
            "required": true,
            "schema": {
              "minLength": 1,
              "type": "string"
            }
          }
        ],
        "requestBody": {
          "content": {
            "multipart/form-data": {
              "schema": {
                "type": "object",
                "properties": {
                  "file": {
                    "type": "string",
                    "description": "File to be uploaded",
                    "format": "binary"
                  }
                }
              },
              "encoding": {
                "file": {
                  "contentType": "application/octet-stream"
                }
              }
            }
          },
          "required": true
        },
        "responses": {
          "202": {
            "description": "Request accepted."
          },
          "400": {
            "description": "Malformed request.",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/ProblemJson"
                }
              }
            }
          },
          "401": {
            "description": "Wrong or missing function key.",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/ProblemJson"
                }
              }
            }
          },
          "403": {
            "description": "Forbidden",
            "content": {
              "application/json": {
                "schema": {
                  "allOf": [],
                  "anyOf": [],
                  "oneOf": []
                }
              }
            }
          },
          "409": {
            "description": "Conflict: duplicate file found.",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/ProblemJson"
                }
              }
            }
          },
          "429": {
            "description": "Too many requests.",
            "content": {
              "text/json": {}
            }
          },
          "500": {
            "description": "Service unavailable.",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/ProblemJson"
                }
              }
            }
          }
        }
      },
      "delete": {
        "tags": [
          "Debt Positions CRUD via file upload API"
        ],
        "summary": "The Organization deletes the debt positions based on IUPD listed in the file.",
        "operationId": "delete-debt-positions-by-file-upload",
        "parameters": [
          {
            "name": "broker-code",
            "in": "path",
            "description": "The broker code",
            "required": true,
            "schema": {
              "minLength": 1,
              "type": "string"
            }
          },
          {
            "name": "organization-fiscal-code",
            "in": "path",
            "description": "The organization fiscal code",
            "required": true,
            "schema": {
              "minLength": 1,
              "type": "string"
            }
          }
        ],
        "requestBody": {
          "content": {
            "multipart/form-data": {
              "schema": {
                "type": "object",
                "properties": {
                  "file": {
                    "type": "string",
                    "description": "File to be uploaded",
                    "format": "binary"
                  }
                }
              },
              "encoding": {
                "file": {
                  "contentType": "application/octet-stream"
                }
              }
            }
          },
          "required": true
        },
        "responses": {
          "202": {
            "description": "Request accepted."
          },
          "400": {
            "description": "Malformed request.",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/ProblemJson"
                }
              }
            }
          },
          "401": {
            "description": "Wrong or missing function key.",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/ProblemJson"
                }
              }
            }
          },
          "403": {
            "description": "Forbidden",
            "content": {
              "application/json": {
                "schema": {
                  "allOf": [],
                  "anyOf": [],
                  "oneOf": []
                }
              }
            }
          },
          "409": {
            "description": "Conflict: duplicate file found.",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/ProblemJson"
                }
              }
            }
          },
          "429": {
            "description": "Too many requests.",
            "content": {
              "text/json": {}
            }
          },
          "500": {
            "description": "Service unavailable.",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/ProblemJson"
                }
              }
            }
          }
        }
      }
    },
    "/brokers/{broker-code}/organizations/{organization-fiscal-code}/debtpositions/file/{file-id}/report": {
      "get": {
        "tags": [
          "Upload Status API"
        ],
        "summary": "Returns the debt positions upload report.",
        "operationId": "get-debt-positions-upload-report",
        "parameters": [
          {
            "name": "broker-code",
            "in": "path",
            "description": "The broker code",
            "required": true,
            "schema": {
              "minLength": 1,
              "type": "string"
            }
          },
          {
            "name": "organization-fiscal-code",
            "in": "path",
            "description": "The organization fiscal code",
            "required": true,
            "schema": {
              "minLength": 1,
              "type": "string"
            }
          },
          {
            "name": "file-id",
            "in": "path",
            "description": "The unique identifier for file upload",
            "required": true,
            "schema": {
              "minLength": 1,
              "type": "string"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "Upload report found.",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/UploadReport"
                }
              }
            }
          },
          "400": {
            "description": "Malformed request.",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/ProblemJson"
                }
              }
            }
          },
          "401": {
            "description": "Wrong or missing function key.",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/ProblemJson"
                }
              }
            }
          },
          "403": {
            "description": "Forbidden",
            "content": {
              "application/json": {
                "schema": {
                  "allOf": [],
                  "anyOf": [],
                  "oneOf": []
                }
              }
            }
          },
          "404": {
            "description": "Upload report not found.",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/ProblemJson"
                }
              }
            }
          },
          "429": {
            "description": "Too many requests.",
            "content": {
              "text/json": {}
            }
          },
          "500": {
            "description": "Service unavailable.",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/ProblemJson"
                }
              }
            }
          }
        }
      }
    },
    "/brokers/{broker-code}/organizations/{organization-fiscal-code}/debtpositions/file/{file-id}/status": {
      "get": {
        "tags": [
          "Upload Status API"
        ],
        "summary": "Returns the debt positions upload status.",
        "operationId": "get-debt-positions-upload-status",
        "parameters": [
          {
            "name": "broker-code",
            "in": "path",
            "description": "The broker code",
            "required": true,
            "schema": {
              "minLength": 1,
              "type": "string"
            }
          },
          {
            "name": "organization-fiscal-code",
            "in": "path",
            "description": "The organization fiscal code",
            "required": true,
            "schema": {
              "minLength": 1,
              "type": "string"
            }
          },
          {
            "name": "file-id",
            "in": "path",
            "description": "The unique identifier for file upload",
            "required": true,
            "schema": {
              "minLength": 1,
              "type": "string"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "Upload found.",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/UploadStatus"
                }
              }
            }
          },
          "400": {
            "description": "Malformed request.",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/ProblemJson"
                }
              }
            }
          },
          "401": {
            "description": "Wrong or missing function key.",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/ProblemJson"
                }
              }
            }
          },
          "403": {
            "description": "Forbidden",
            "content": {
              "application/json": {
                "schema": {
                  "allOf": [],
                  "anyOf": [],
                  "oneOf": []
                }
              }
            }
          },
          "404": {
            "description": "Upload not found.",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/ProblemJson"
                }
              }
            }
          },
          "429": {
            "description": "Too many requests.",
            "content": {
              "text/json": {}
            }
          },
          "500": {
            "description": "Service unavailable.",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/ProblemJson"
                }
              }
            }
          }
        }
      }
    },
    "/info": {
      "get": {
        "tags": [
          "Health check"
        ],
        "summary": "health check",
        "description": "Return OK if application is started",
        "operationId": "healthCheck",
        "responses": {
          "200": {
            "description": "OK",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/AppInfo"
                }
              }
            }
          },
          "400": {
            "description": "Bad Request",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/ProblemJson"
                }
              }
            }
          },
          "401": {
            "description": "Unauthorized",
            "content": {
              "application/json": {
                "schema": {
                  "allOf": [],
                  "anyOf": [],
                  "oneOf": []
                }
              }
            }
          },
          "403": {
            "description": "Forbidden",
            "content": {
              "application/json": {
                "schema": {
                  "allOf": [],
                  "anyOf": [],
                  "oneOf": []
                }
              }
            }
          },
          "429": {
            "description": "Too many requests.",
            "content": {
              "text/json": {}
            }
          },
          "500": {
            "description": "Service unavailable",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/ProblemJson"
                }
              }
            }
          }
        }
      }
    }
  },
  "components": {
    "schemas": {
      "AppInfo": {
        "type": "object",
        "properties": {
          "name": {
            "type": "string"
          },
          "version": {
            "type": "string"
          },
          "environment": {
            "type": "string"
          }
        }
      },
      "ProblemJson": {
        "type": "object",
        "properties": {
          "title": {
            "type": "string",
            "description": "A short, summary of the problem type. Written in english and readable for engineers (usually not suited for non technical stakeholders and not localized); example: Service Unavailable"
          },
          "status": {
            "type": "integer",
            "description": "The HTTP status code generated by the origin server for this occurrence of the problem.",
            "format": "int32",
            "example": 200
          },
          "detail": {
            "type": "string",
            "description": "A human readable explanation specific to this occurrence of the problem.",
            "example": "There was an error processing the request"
          }
        },
        "description": "Object returned as response in case of an error."
      },
      "ResponseEntry": {
        "type": "object",
        "properties": {
          "statusCode": {
            "type": "integer",
            "format": "int32",
            "example": 400
          },
          "statusMessage": {
            "type": "string",
            "example": "Bad request caused by invalid email address"
          },
          "requestIDs": {
            "type": "array",
            "items": {
              "type": "string"
            }
          }
        }
      },
      "UploadReport": {
        "type": "object",
        "properties": {
          "uploadID": {
            "type": "string"
          },
          "processedItem": {
            "type": "integer",
            "format": "int32"
          },
          "submittedItem": {
            "type": "integer",
            "format": "int32"
          },
          "responses": {
            "type": "array",
            "items": {
              "$ref": "#/components/schemas/ResponseEntry"
            }
          },
          "startTime": {
            "type": "string",
            "format": "date-time",
            "example": "2024-10-08T14:55:16.302Z"
          },
          "endTime": {
            "type": "string",
            "format": "date-time",
            "example": "2024-10-08T14:55:16.302Z"
          }
        }
      },
      "UploadStatus": {
        "type": "object",
        "properties": {
          "uploadID": {
            "type": "string"
          },
          "processedItem": {
            "type": "integer",
            "format": "int32"
          },
          "submittedItem": {
            "type": "integer",
            "format": "int32"
          },
          "startTime": {
            "type": "string",
            "format": "date-time",
            "example": "2024-10-08T14:55:16.302Z"
          }
        }
      }
    },
    "securitySchemes": {
      "Ocp-Apim-Subscription-Key": {
        "type": "apiKey",
        "name": "Ocp-Apim-Subscription-Key",
        "in": "header"
      }
    }
  }
}
