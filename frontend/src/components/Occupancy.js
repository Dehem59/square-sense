class OccupancyComponent{
    constructor(data, location) {
        this.data = data;
        this.location = location;
    }

    generateTemplate(){
        this.location.classList.remove("d-none");
        return `
        <div>
            <p>${this.data['sensorName']} reports room occupancy of ${this.data['inside']} people</p>        
        </div>`
    }

    refresh(){
        this.location.innerHTML = this.generateTemplate()
    }
}
