// frontend/src/App.js

import React, { Component } from "react";
import SearchResults from "./components/loadingModal";
import axios from "axios";


class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      modal: true,
      topicBox: null,
    };

    this.publish = this.publish.bind(this);
    this.handleChange = this.handleChange.bind(this);
  }

  handleChange({ target }) {
    this.setState({
      [target.name]: target.value
    });
  }

  publish() {
    console.log( this.state.topicBox);
  }

  componentDidMount() {
    this.refreshList();
  }
  refreshList = () => {
    axios
      .get("api/")
      .then(res => this.setState({ todoList: res.data }))
      .catch(err => console.log(err));
  };

  toggle = () => {
    this.setState({ modal: !this.state.modal });
  };
  
  render() {
    return (
      <main className="content">
        <h1 className="text-black text-uppercase text-center my-4">#Codechella2020 APP</h1>
        <div className="row ">
          <div className="col-md-6 col-sm-10 mx-auto p-0">
            <div className="card p-3">
              <div className="">
              <form className="text-center col-md-6 col-sm-10 mx-auto p-0">
                 <label>
                  <input type="text" name="title" />
                </label>
                <input type="submit" value="Search"  onclick="this.publish"/> 
              </form>
              {this.state.modal ? (
          <SearchResults
            activeItem={this.state.activeItem}
            toggle={this.toggle}
            value={ this.state.topicBox }
            onChange={ this.handleChange } 
          />
        ) : null}
              </div>
              <ul className="list-group list-group-flush">
              </ul>
            </div>
          </div>
        </div>

      </main>
    );
  }
}
export default App;