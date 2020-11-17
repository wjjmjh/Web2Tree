__contributors__ = ["Stephen Ka-Wah Ma"]

react_ts_class_template = """
class {class_name} extends Component<{props_types}, {states_types}> {
  {constructor}
  
  {body}

  render() {
    return (
      {skeleton}
    );
  }
}
"""
