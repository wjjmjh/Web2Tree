# basic React component class
template1 = """
class {class_name} extends Component<{props_types}, {states_types}> {
  constructor(props: {props_types}) {
    super(props);
    this.state: states_types= {};
  }

  render() {
    return (
      {skeleton}
    );
  }
}
"""
