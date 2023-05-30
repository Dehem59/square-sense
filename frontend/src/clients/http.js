
class HttpClient{
    __authorizedContentType = {"json": "application/json", "form-data": "multipart/form-data"};

    constructor(contentType="json") {
        if (!contentType in this.__authorizedContentType) throw new TypeError("content-type is unknown");
        this.contentType = contentType;
    }

    getUrl(baseUrl, uri=null, params=null){
        let finalUrl;
        if (uri != null){
            if (baseUrl.endsWith("/")){
                if (uri.startsWith("/")){
                    finalUrl = baseUrl + uri.slice(1);
                } else {
                    finalUrl = baseUrl + uri;
                }
            } else {
                if (uri.startsWith("/")){
                    finalUrl = baseUrl + uri;
                } else {
                    finalUrl = baseUrl + "/" + uri;
                }
            }
        } else {
            finalUrl = baseUrl
        }
        if (params !== null){
            finalUrl += "?" + Object.entries(
                params
            ).map(
                ([key, value])=> key + "=" + value
            ).join("&")
        }
        return finalUrl
    }

    getHeaders(){
        return {"Content-Type": this.__authorizedContentType[this.contentType]};
    }

    getEncodedData(data){
        if (this.contentType === "json"){
            return JSON.stringify(data)
        }
        else if (this.contentType === "form-data"){
            if (data instanceof FormData){
                return data;
            }
            throw new TypeError("Need to convert JS object to FormData")
        }
    }

    getHttpConfig(method, data=null){
        let config = {
            credentials: "same-origin", method: method, headers: this.getHeaders(),
        }
        if (data !== null){
            config.body = this.getEncodedData(data);
        }
        return config;
    }

    async request(method, url, data=null){
        let config = this.getHttpConfig(method, data)
        return await fetch(url, config);
    }

    async post(url, data=null){
        return await this.request("post", url, data)
    }

    async get(url, data=null){
        return this.request("get", url, data)
    }

    async patch(url, data=null){
        return await this.request("patch", url, data);
    }

    async put(url, data=null){
        return await this.request("put", url, data);
    }

    async delete(url, data=null){
        return await this.request("delete", url, data);
    }
}

