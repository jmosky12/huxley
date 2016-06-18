/**
* Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
* Use of this source code is governed by a BSD License (see LICENSE).
*
* @jsx React.DOM
+*/

'use strict';

var $ = require('jquery');
var React = require('react');
var Router = require('react-router');

var AssignmentStore = require('../stores/AssignmentStore');
var Button = require('./Button');
var CommitteeStore = require('../stores/CommitteeStore');
var CountryStore = require('../stores/CountryStore');
var CurrentUserStore = require('../stores/CurrentUserStore');
var DelegateStore = require('../stores/DelegateStore');
var CurrentUserActions = require('../actions/CurrentUserActions');
var InnerView = require('./InnerView');

var AdvisorRosterView = React.createClass({
  mixins: [
    Router.Navigation,
  ],

  getInitialState: function() {
    return {
      assignments: [],
      delegates: [],
      committees: {},
      countries: {},
      loading: false,
      errors: {},
      name: '',
      email: '',
      summary: '',
    };
  },

  componentWillMount: function() {
    var user = CurrentUserStore.getCurrentUser();
    AssignmentStore.getAssignments(user.school.id, function(assignments) {
      this.setState({assignments: assignments.filter(
        function(assignment) {
          return !assignment.rejected
        }
      )});
    }.bind(this));
    CommitteeStore.getCommittees(function(committees) {
      var new_committees = {};
      for (var i = 0; i < committees.length; i++) {
        new_committees[committees[i].id] = committees[i];
      }
      this.setState({committees: new_committees});
    }.bind(this));
    CountryStore.getCountries(function(countries) {
      var new_countries = {};
      for (var i = 0; i <countries.length; i++) {
        new_countries[countries[i].id] = countries[i];
      }
      this.setState({countries: new_countries})
    }.bind(this));
    DelegateStore.getDelegates(user.school.id, function(delegates) {
      this.setState({delegates: delegates});
    }.bind(this));
  },

  render: function() {
    return (
      <InnerView>
        <h2>Roster</h2>
        <p>
          REVERT BACK
          // Here you can add your schools delegates to your roster.
          Any comments that chairs have about your delegate will appear here.
        </p>
        <form>
          <div className="tablemenu header" />
          <div className="table-container">
            <table className="table highlight-cells">
              <tr>
                <th>Delegate</th>
                <th>Email</th>
                <th>Summary</th>
              </tr>
              {this.renderRosterRows()}
            </table>
          </div>
        </form>
        <div>
          <Button onclick={this._addDelegatePressed}>Add Delegate</Button>
        </div>
      </InnerView>
    );
  },

  renderRosterRows: function() {
    var committees = this.state.committees;
    var countries = this.state.countries;
    console.dir(this.state.delegates[0])
    return this.state.delegates.map(function(delegate) {
      return (
        <tr>
          <td>{delegate.name}</td>
          <td>{delegate.email}</td>
          <td>{delegate.summary}</td>
          <td>
            <Button>Delete</Button>
          </td>
        </tr>
      )
    }.bind(this));
  },

  _addDelegatePressed: function() {
    return (
      <form>
        Name: <input type="text" placeholder="Name" valueLink={this.linkState('name')} /><br>
        Email: <input type="text" placeholder="Email" valueLink={this.linkState('email')}/><br>
        Summary: <input type="text" placeholder="Summary" valueLink={this.linkState('summary')}/><br>
        <input type="submit" value="Submit" onclick={this._handleSubmit} />
      </form>
    )
  },

  _handleSubmit: function(data) {
    this.setState({loading: true});
    $.ajax({
      type: 'POST',
      url: '/api/delegate',
      data: {
        name: this.state.name,
        email: this.state.email,
        summary: this.state.summary
      },
      success: this._handleSuccess,
      error: this._handleError,
      dataType: 'json'
    });
    event.preventDefault();
  },

  _handleSuccess: function(data, status, jqXHR) {
    console.log("success!");
    //REMOVE SUBMIT FORM FROM SCREEN
  },

  _handleError: function(jqXHR, status, error) {
    var response = jqXHR.responseJSON;
    if (!response) {
      return;
    }

    this.setState({
      errors: response,
      loading: false
    }.bind(this));
  }

});

module.exports = AdvisorRosterView;
