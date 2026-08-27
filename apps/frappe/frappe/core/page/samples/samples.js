frappe.pages['samples'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Sample',
		single_column: true
	});

	page.main.html(`
		<div class="sample-container">
			<div id="sample-output" style="margin-top: 10px;"></div>
		</div>
	`);

frappe.call({
	method: 'frappe.client.get_list',
	args: {
		doctype: 'Workspace',
		fields: ['name', 'title', 'module'],
		limit_page_length: 0
	},
	callback: function(r) {
		if (r.message) {
			render_table(r.message);
		}
	}
});

function render_table(rows) {
	var html = `
		<table class="table table-bordered">
			<thead>
				<tr>
					<th>Name</th>
					<th>Title</th>
					<th>Module</th>
				</tr>
			</thead>
			<tbody>
				${rows.map(row => `
					<tr>
						<td>${frappe.utils.escape_html(row.name || '')}</td>
						<td>${frappe.utils.escape_html(row.title || '')}</td>
						<td>${frappe.utils.escape_html(row.module || '')}</td>
					</tr>
				`).join('')}
			</tbody>
		</table>
	`;
	page.main.find('#sample-output').html(html);
}
};