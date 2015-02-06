<dl class="dl-horizontal">
	<dt>Nom de la tache :</dt>
	<dd>{{headers.JobName}}</dd>
	
	<dt>Nom du fichier :</dt>
	<dd>{{filename}}</dd>

	<dt>Date de création :</dt>
	<dd>{{date date "DD/MM/YYYY à HH:mm"}}</dd>

	<dt>Taille du fichier :</dt>
	<dd>{{numeral weight "0.0b"}}</dd>

	<dt>Dimensions de la tache :</dt>
	<dd>
		{{numeral headers.Size.width "0.0"}}x{{numeral headers.Size.height "0.0"}}mm <em>({{headers.px_width}}x{{headers.px_height}}px)</em>
	</dd>

	<dt>Résolution :</dt>
	<dd>{{headers.Resolution}}dpi</dd>

	<dt>Type de gravure :</dt>
	<dd>
		{{#if headers.bmp}} 
			{{headers.ProcessMode}} 
		{{else}} 
			Aucune : travail de découpe seulement 
		{{/if}}
	</dd>
	
	<dt>Découpe : </dt>
	<dd>
		{{#if headers.cut}} 
			{{#each headers.cut}}
				<div class="colorbox" style="background-color:{{this}}" title="{{this}}">&nbsp;</div>
			{{/each}}
		{{else}} 
			Aucune découpe
		{{/if}}
	
	</dd>
</dl>
