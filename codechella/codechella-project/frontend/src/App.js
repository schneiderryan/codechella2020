// frontend/src/App.js

import React, { Component } from "react";
import SearchResults from "./components/loadingModal";

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      modal: false,
    };
  }
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
                <input type="submit" value="Search"  /> 
              </form>
              {this.state.modal ? (
          <SearchResults
            activeItem={this.state.activeItem}
            toggle={this.toggle}
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