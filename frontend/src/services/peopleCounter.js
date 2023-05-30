class PeopleCounterService{
    host = "http://127.0.0.1:5000"
    webhookApi = "/api/webhook"
    occupancyApi = "/api/occupancy"

    constructor() {
        this.client = new HttpClient();
        this.locationId = "occupancyDiv";
    }

    getComponent(data){
        return new OccupancyComponent(data, document.getElementById(this.locationId))
    }

    async submit(sensorName){
        let response = await this.client.get(
            this.client.getUrl(
                this.host, this.occupancyApi, {"sensor": sensorName}
            )
        )
        let data = await response.json();
        data["sensorName"] = sensorName;
        let component = this.getComponent(data)
        component.refresh();
    }

    async createRecord(data){
        return await this.client.post(this.client.getUrl(this.host, this.webhookApi), data)
    }

    async addSelectOptions(selectElement){
        let response = await this.client.get(this.client.getUrl(this.host, this.webhookApi))
        let data = await response.json()
        selectElement.innerHTML = data.map(
            el => {
                return "<option value='" + el.name + "'>" + el.name + "</option>";
            }
        );
    }
}