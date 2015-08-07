<%inherit file="/base.mako"/>
<%namespace file="/message.mako" import="render_msg" />
<%namespace file="/spark_base.mako" import="make_sparkline" />
<%namespace file="/sorting_base.mako" import="get_sort_url, get_css" />

%if message:
    ${render_msg( message, 'done' )}
%endif

${get_css()}

<!--jobs_per_month_all.mako-->
<div class="toolForm">
    <div class="toolFormBody">
        <h4 align="center">Jobs Per Month</h4>
        <h5 align="center">Click Month to view details. Graph goes from the 1st to the last of the month.</h5>
        <table align="center" width="60%" class="colored">
            %if len( jobs ) == 0:
                <tr><td colspan="4">There are no jobs.</td></tr>
            %else:
                <tr class="header">
                    <td class="third_width">
                        ${get_sort_url(sort_id, order, 'date', 'jobs', 'per_month_all', 'Month')}
                        <span class='dir_arrow date'>${arrow}</span>
                    </td>
                    %if is_user_jobs_only:
    					<td class="third_width">
                            ${get_sort_url(sort_id, order, 'total_jobs', 'jobs', 'per_month_all', 'User Jobs')}
                            <span class='dir_arrow total_jobs'>${arrow}</span>
                        </td>
					%else:
	                    <td class="third_width">
                            ${get_sort_url(sort_id, order, 'total_jobs', 'jobs', 'per_month_all', 'User and Monitor Jobs')}
                            <span class='dir_arrow total_jobs'>${arrow}</span>
                        </td>
	                %endif
                    <td></td>
                </tr>
                <% ctr = 0 %>
                %for job in jobs:
                    <% key = str(job[2]) + str(job[3]) %>
                    %if ctr % 2 == 1:
                        <tr class="odd_row">
                    %else:
                        <tr class="tr">
                    %endif
                        <td><a href="${h.url_for( controller='jobs', action='specified_month_all', specified_date=job[0]+'-01', sort_id='default', order='default' )}">${job[2]} ${job[3]}</a></td>
                        <td>${job[1]}</td>
                        ${make_sparkline(key, trends[key], "bar", "/ day")}
                        <td id="${key}"></td>
                    </tr>
                    <% ctr += 1 %>
                %endfor
            %endif
        </table>
    </div>
</div>
<!--jobs_per_month_all.mako-->
