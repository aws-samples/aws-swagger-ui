const express = require('express')
const serverless = require('serverless-http')
const swaggerUI = require('swagger-ui-express')

let AWS = require('aws-sdk');
let s3 = new AWS.S3({
    signatureVersion: 'v4',
});

const app = express()

module.exports.handler = async (event, context) => {
    const signedUrl = s3.getSignedUrl(
        'getObject',
        {
            Bucket: process.env.BUCKET_NAME,
            Key: process.env.KEY_NAME,
            Expires: 30
        }
    );

    let options = {
        swaggerOptions: {
            url: signedUrl
        }
    }

    app.use('/api-docs', swaggerUI.serve, swaggerUI.setup(null, options))
    const handler = serverless(app);

    return await handler(event, context)
}