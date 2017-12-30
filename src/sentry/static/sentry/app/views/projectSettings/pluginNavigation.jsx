import React from 'react';

import withPlugins from '../../utils/withPlugins';

const PluginNavigation = React.createClass({
  render() {
    let {urlRoot, plugins} = this.props;

    if (!plugins || !plugins.plugins) return null;
    let enabledPlugins = plugins.plugins.filter(p => p.enabled && p.hasConfiguration);

    if (!enabledPlugins.length) return null;

    return (
      <div>
        {enabledPlugins.map(({id, name}) => (
          <li key={id}>
            <a href={`${urlRoot}/plugins/${id}/`}>{name}</a>
          </li>
        ))}
      </div>
    );
  },
});

export default withPlugins(PluginNavigation);
