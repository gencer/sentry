import PropTypes from 'prop-types';
import React from 'react';

import TimeSince from '../../components/timeSince';
import ConfigStore from '../../stores/configStore';
import LinkWithConfirmation from '../../components/linkWithConfirmation';
import {t} from '../../locale';
import marked from '../../utils/marked';

class Note extends React.Component {
  static propTypes = {
    author: PropTypes.object.isRequired,
    item: PropTypes.object.isRequired,
    onEdit: PropTypes.func.isRequired,
    onDelete: PropTypes.func.isRequired,
  };

  canEdit = () => {
    let user = ConfigStore.get('user');
    return user.isSuperuser || user.id === this.props.item.user.id;
  };

  render() {
    let {item, author, onEdit, onDelete} = this.props;

    let noteBody = marked(item.data.text);
    return (
      <div>
        <TimeSince date={item.dateCreated} />
        <div className="activity-author">
          {author.name}
          {this.canEdit() && (
            <span className="editor-tools">
              <a onClick={onEdit}>{t('Edit')}</a>
              <LinkWithConfirmation
                className="danger"
                message={t('Are you sure you wish to delete this comment?')}
                onConfirm={onDelete}
              >
                {t('Remove')}
              </LinkWithConfirmation>
            </span>
          )}
        </div>
        <div dangerouslySetInnerHTML={{__html: noteBody}} />
      </div>
    );
  }
}

export default Note;
