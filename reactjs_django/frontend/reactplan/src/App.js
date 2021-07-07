import React, { Component } from 'react'
import Plan from './Plan'
import './App.css';
import '../node_modules/bootstrap/dist/css/bootstrap.min.css'
import axios from 'axios'

//Axios Instance
const ai = axios.create({
  baseURL: 'http://127.0.0.1:8000/api'
})
class App extends Component {
  state= {
    items: [],
    text: ""
  }
  showPlan = () => {
    ai.get('/list/')
    .then((res)=>{
      this.setState({ items: res.data })
    })
  }
  addPlan = (d) => {
    if (this.state.text !==""){
      ai.post('/create/', d)
      .then((res)=>{
        this.setState({ text: '' })
        this.showPlan()
      })
    }
  }
  handleChange = e =>{
    this.setState({ text: e.target.value })
  }
  handleAdd = e =>{
    let dt = {item: this.state.text}
    this.addPlan(dt)
  }
  handleDelete = id => {
    console.log("Deleted", id)
    ai.delete(`/delete/${id}`)
    .then((res) => {
      this.showPlan()
    })
  }
  componentDidMount(){
    this.showPlan();
  }
  render() {
    return (
      <div className="container-fluid my-5">
        <div className="row">
          <div className="col-sm-6 text-white shadow-lg p-3 mx-auto">
            <h2 className="text-center mx-auto"> Today's Plan </h2>
            <div className="col-sm-12 mx-auto">
              <input type="text" className="form-control" placeholder="write your text" value={this.state.text} onChange={this.handleChange} />
            </div>
            <div className="col-2 mx-auto my-auto">
              <button className="btn btn-warning px-5 fw-bold my-2" onClick={this.handleAdd}>Add</button>
            </div>
            <div className="container-field">
              <ul class="list-unstyled row m-5">
                {
                this.state.items.map((value, i)=>{
                  return <Plan key={i} id={value.id} value={value.item} sendData ={this.handleDelete} />
                })
                }
              </ul>
            </div>
          </div>
        </div>
      </div>
    )
  }
}
export default App;