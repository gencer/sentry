import PropTypes from 'prop-types';
import React from 'react';

import IconGithub from '../../icons/icon-github';
import IconBitbucket from '../../icons/icon-bitbucket';

const CommitLink = React.createClass({
  propTypes: {
    commitId: PropTypes.string,
    repository: PropTypes.object,
    inline: PropTypes.bool,
  },

  getCommitUrl() {
    // TODO(jess): move this to plugins
    if (this.props.repository.provider.id === 'github') {
      return this.props.repository.url + '/commit/' + this.props.commitId;
    }
    if (this.props.repository.provider.id === 'bitbucket') {
      return this.props.repository.url + '/commits/' + this.props.commitId;
    }
    return undefined;
  },

  render() {
    let commitUrl = this.getCommitUrl();
    let shortId = this.props.commitId.slice(0, 7);

    return commitUrl ? (
      <a
        className={this.props.inline ? 'inline-commit' : 'btn btn-default btn-sm'}
        href={commitUrl}
        target="_blank"
      >
        {this.props.repository.provider.id == 'github' && (
          <IconGithub size="16" style={{verticalAlign: 'text-top'}} />
        )}
        {this.props.repository.provider.id == 'bitbucket' && (
          <IconBitbucket size="16" style={{verticalAlign: 'text-top'}} />
        )}
        &nbsp;
        {this.props.inline ? '' : ' '}
        {shortId}
      </a>
    ) : (
      <span>{shortId}</span>
    );
  },
});
export default CommitLink;
