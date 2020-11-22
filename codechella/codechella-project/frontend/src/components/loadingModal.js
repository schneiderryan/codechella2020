// frontend/src/components/Modal.js

import React, { Component } from "react";
import {
  Modal,
  ModalHeader,
  ModalBody,
  ModalFooter,
  Form,
  FormGroup,
  Label
} from "reactstrap";

export default class searchResults extends Component {
  constructor(props) {
	super(props);
	this.state = {
	  activeItem: this.props.activeItem
	};
  }
  handleChange = e => {
	let { name, value } = e.target;
	if (e.target.type === "checkbox") {
	  value = e.target.checked;
	}
	const activeItem = { ...this.state.activeItem, [name]: value };
	this.setState({ activeItem });
  };
  render() {
	const { toggle } = this.props;
	return (
	  <Modal isOpen={true} toggle={toggle}>
		<ModalHeader toggle={toggle}> Search Results for Placeholder </ModalHeader>
		<ModalBody>
		  <Form>
			  {/* TODO: pass it
			  			activeItem 
			  			title 
						  Neutral results
						  Positive Results
						  Negative results
				*/}
			<FormGroup>
				<Label for="title">X tweets of Placeholder are positive</Label>
				<Label for="title">Y tweets of Placeholder are negative</Label>
				<Label for="title">Z tweets of Placeholder are neutral</Label>

			</FormGroup>
			<FormGroup check>
			  <Label for="completed">

				

			  </Label>
			</FormGroup>
		  </Form>
		</ModalBody>
		<ModalFooter>
		</ModalFooter>
	  </Modal>
	);
  }
}