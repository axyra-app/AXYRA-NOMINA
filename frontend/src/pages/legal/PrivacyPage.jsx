import { ArrowLeft } from 'lucide-react'
import { useNavigate } from 'react-router-dom'

export default function PrivacyPage() {
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
          <h1 className="text-3xl font-bold text-gray-900">Política de Privacidad</h1>
          <p className="text-gray-500 text-sm mt-2">Última actualización: 7 de enero de 2026</p>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-4xl mx-auto px-4 py-12">
        <div className="prose prose-sm max-w-none text-gray-700 space-y-8">
          {/* Introduction */}
          <section>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">1. Introducción</h2>
            <p>
              Axyra ("nosotros", "nuestro" o "nos") opera la plataforma de gestión de nóminas 
              Axyra. Esta página le informa sobre nuestras políticas con respecto a la recopilación, 
              el uso y la divulgación de datos personales cuando utiliza nuestro Servicio.
            </p>
          </section>

          {/* Information Collection */}
          <section>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">2. Recopilación de Información</h2>
            <p>Recopilamos varios tipos de información para diversos propósitos:</p>
            
            <h3 className="text-lg font-semibold text-gray-800 mt-6 mb-3">Información Personal</h3>
            <p>
              Cuando se registra, recopilamos información como su nombre, dirección de correo 
              electrónico, número de teléfono y otra información de contacto.
            </p>

            <h3 className="text-lg font-semibold text-gray-800 mt-6 mb-3">Datos de Empleados</h3>
            <p>
              Como parte de la funcionalidad de nuestro Servicio, usted puede cargar información 
              de empleados, incluidos nombres, números de identificación, salarios y datos de 
              nómina.
            </p>

            <h3 className="text-lg font-semibold text-gray-800 mt-6 mb-3">Datos de Uso</h3>
            <p>
              Recopilamos automáticamente cierta información sobre su dispositivo cuando utiliza 
              nuestro Servicio, incluyendo direcciones IP, tipo de navegador, páginas visitadas y 
              tiempo de acceso.
            </p>
          </section>

          {/* Use of Information */}
          <section>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">3. Uso de Información</h2>
            <p>Utilizamos la información recopilada para:</p>
            <ul className="list-disc pl-6 space-y-2 mt-4">
              <li>Proporcionar, mantener y mejorar el Servicio</li>
              <li>Procesar transacciones y enviar información relacionada</li>
              <li>Enviar correos electrónicos técnicos, de soporte y administrativos</li>
              <li>Responder a sus comentarios, preguntas y solicitudes</li>
              <li>Monitorear y analizar tendencias, uso y actividades del Servicio</li>
              <li>Detectar y prevenir problemas técnicos y fraude</li>
              <li>Cumplir con obligaciones legales</li>
            </ul>
          </section>

          {/* Data Security */}
          <section>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">4. Seguridad de Datos</h2>
            <p>
              La seguridad de sus datos es importante para nosotros. Utilizamos medidas de seguridad 
              técnicas, administrativas y físicas apropiadas para proteger su información personal 
              contra acceso no autorizado, alteración, divulgación o destrucción.
            </p>
            <p className="mt-4">
              Sin embargo, ningún método de transmisión por Internet o almacenamiento electrónico 
              es 100% seguro. Aunque hacemos todo lo posible para proteger su información personal, 
              no podemos garantizar su seguridad absoluta.
            </p>
          </section>

          {/* Data Retention */}
          <section>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">5. Retención de Datos</h2>
            <p>
              Retenemos datos personales durante el tiempo que sea necesario para proporcionar 
              nuestros Servicios y cumplir con las obligaciones legales. Cuando los datos ya no 
              son necesarios, se eliminan o se anonimalizan.
            </p>
          </section>

          {/* Third Parties */}
          <section>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">6. Divulgación a Terceros</h2>
            <p>
              No vendemos, comerciamos ni transferimos su información personal a terceros sin su 
              consentimiento, excepto según sea necesario para:
            </p>
            <ul className="list-disc pl-6 space-y-2 mt-4">
              <li>Cumplir con la ley o proteger nuestros derechos</li>
              <li>Proveedores de servicios confiables que nos ayudan a operar nuestro Servicio</li>
              <li>Transacciones comerciales autorizadas</li>
            </ul>
          </section>

          {/* User Rights */}
          <section>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">7. Derechos del Usuario</h2>
            <p>Según la ley aplicable, usted puede tener derechos que incluyen:</p>
            <ul className="list-disc pl-6 space-y-2 mt-4">
              <li>Acceder a sus datos personales</li>
              <li>Corregir datos inexactos</li>
              <li>Solicitar la eliminación de datos</li>
              <li>Objetar al procesamiento de sus datos</li>
              <li>Solicitar la portabilidad de datos</li>
            </ul>
            <p className="mt-4">
              Para ejercer estos derechos, contáctenos a través de nuestro sitio web.
            </p>
          </section>

          {/* Cookies */}
          <section>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">8. Cookies</h2>
            <p>
              Utilizamos cookies y tecnologías similares para mejorar su experiencia. Estas pueden 
              incluir cookies esenciales para la funcionalidad, cookies analíticas y cookies de 
              preferencia.
            </p>
          </section>

          {/* Children */}
          <section>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">9. Protección de Menores</h2>
            <p>
              Nuestro Servicio no está dirigido a menores de 13 años. No recopilamos información 
              personal de personas menores de 13 años de manera intencional. Si nos enteramos de 
              que hemos recopilado dicha información, la eliminaremos inmediatamente.
            </p>
          </section>

          {/* Changes */}
          <section>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">10. Cambios en esta Política</h2>
            <p>
              Podemos actualizar nuestra Política de Privacidad de vez en cuando. Se le notificará 
              de cualquier cambio publicando la nueva Política de Privacidad en esta página y 
              actualizando la fecha de "Última actualización".
            </p>
          </section>

          {/* Contact */}
          <section>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">11. Contacto</h2>
            <p>
              Si tiene preguntas sobre esta Política de Privacidad, contáctenos a través de 
              nuestro sitio web o envíe un correo a privacy@axyra.com
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
