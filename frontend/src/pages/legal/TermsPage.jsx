import { ArrowLeft } from 'lucide-react'
import { useNavigate } from 'react-router-dom'

export default function TermsPage() {
  const navigate = useNavigate()

  return (
    <div className="min-h-screen bg-gray-50 pt-8 pb-16">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 sticky top-0 z-10">
        <div className="max-w-4xl mx-auto px-4 py-4">
          <button
            onClick={() => navigate(-1)}
            className="flex items-center gap-2 text-gray-600 hover:text-gray-900 mb-4"
          >
            <ArrowLeft size={20} />
            <span>Volver</span>
          </button>
          <h1 className="text-3xl font-bold text-gray-900">Términos y Condiciones</h1>
          <p className="text-gray-500 text-sm mt-2">Última actualización: 7 de enero de 2026</p>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-4xl mx-auto px-4 py-12">
        <div className="prose prose-sm max-w-none text-gray-700 space-y-8">
          {/* Introduction */}
          <section>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">1. Aceptación de Términos</h2>
            <p>
              Al acceder y utilizar Axyra - Sistema de Gestión de Nóminas ("el Servicio"), 
              usted acepta estar vinculado por estos Términos y Condiciones. Si no está de acuerdo 
              con alguna parte de estos términos, entonces no puede utilizar nuestro Servicio.
            </p>
          </section>

          {/* License */}
          <section>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">2. Licencia de Uso</h2>
            <p>
              Le otorgamos una licencia limitada, no exclusiva y revocable para usar nuestro 
              Servicio de conformidad con estos Términos y Condiciones. Usted no debe:
            </p>
            <ul className="list-disc pl-6 space-y-2 mt-4">
              <li>Reproducir, duplicar, copiar o vender el Servicio</li>
              <li>Acceder al Servicio con el propósito de construir un producto o servicio competidor</li>
              <li>Usar el Servicio de manera que pueda dañar, deshabilitar o sobrecargar el Servicio</li>
              <li>Intentar obtener acceso no autorizado a cualquier parte del Servicio</li>
            </ul>
          </section>

          {/* User Accounts */}
          <section>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">3. Cuentas de Usuario</h2>
            <p>
              Cuando crea una cuenta con nosotros, debe proporcionar información que sea precisa, 
              completa y actual en todo momento. El incumplimiento de esto constituye una violación 
              de los Términos y puede resultar en la terminación inmediata de su cuenta.
            </p>
            <p className="mt-4">
              Usted es responsable de mantener la confidencialidad de su cuenta y contraseña y 
              es totalmente responsable de todas las actividades que ocurran bajo su cuenta.
            </p>
          </section>

          {/* Data Protection */}
          <section>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">4. Protección de Datos</h2>
            <p>
              Usted reconoce que al utilizar nuestro Servicio, está compartiendo información 
              sensible, incluida información de empleados y nómina. Nos comprometemos a mantener 
              su información segura de conformidad con nuestras políticas de privacidad y las 
              leyes aplicables de protección de datos.
            </p>
          </section>

          {/* User Responsibilities */}
          <section>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">5. Responsabilidades del Usuario</h2>
            <p>
              Usted se compromete a utilizar el Servicio de manera legal y de acuerdo con todas 
              las leyes y regulaciones aplicables. Específicamente:
            </p>
            <ul className="list-disc pl-6 space-y-2 mt-4">
              <li>Cumplerá con todas las leyes laborales y de nómina aplicables</li>
              <li>No utilizará el Servicio para ningún propósito ilegal</li>
              <li>Mantendrá la seguridad de su información de acceso</li>
              <li>Será responsable de la precisión de los datos que ingresa</li>
            </ul>
          </section>

          {/* Liability Limitation */}
          <section>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">6. Limitación de Responsabilidad</h2>
            <p>
              En ningún caso Axyra, sus directores, empleados o agentes serán responsables de 
              daños indirectos, incidentales, especiales, consecuentes o punitivos, incluyendo 
              pero no limitado a pérdida de ganancias, pérdida de datos o pérdida de uso.
            </p>
          </section>

          {/* Disclaimer */}
          <section>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">7. Descargo de Responsabilidad</h2>
            <p>
              El Servicio se proporciona "TAL CUAL" sin garantía de ningún tipo. Axyra no 
              garantiza que el Servicio sea continuo, ininterrumpido o libre de errores.
            </p>
          </section>

          {/* Termination */}
          <section>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">8. Terminación</h2>
            <p>
              Podemos terminar o suspender su cuenta y acceso al Servicio de inmediato, sin 
              previo aviso o responsabilidad, por cualquier razón, incluyendo si infringe los 
              Términos y Condiciones.
            </p>
          </section>

          {/* Changes to Terms */}
          <section>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">9. Cambios en los Términos</h2>
            <p>
              Nos reservamos el derecho de modificar o reemplazar estos Términos en cualquier 
              momento. Si una revisión es material, proporcionaremos un aviso de al menos 30 
              días antes de que entren en vigencia los nuevos términos.
            </p>
          </section>

          {/* Contact */}
          <section>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">10. Contacto</h2>
            <p>
              Si tiene preguntas sobre estos Términos y Condiciones, por favor contáctenos a 
              través de nuestro sitio web o envíe un correo a support@axyra.com
            </p>
          </section>

          {/* Footer */}
          <div className="pt-8 border-t border-gray-200 text-sm text-gray-500">
            <p>
              © 2026 Axyra - Sistema de Gestión de Nóminas. Todos los derechos reservados.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
